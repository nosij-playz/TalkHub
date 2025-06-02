import eventlet
eventlet.monkey_patch()  # MUST BE FIRST — ensures non-blocking I/O

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import random
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

# Mappings
user_id_to_sid = {}
sid_to_user_id = {}
issued_ids = set()

# -------------------------------
# Route: Health Check
# -------------------------------
@app.route('/')
def index():
    return jsonify({"message": "Private Chat Server is Running!"})

# -------------------------------
# Route: Get a New Relay ID
# -------------------------------
@app.route('/new-id')
def generate_new_relay_id():
    while True:
        new_id = str(random.randint(1000, 9999))
        if new_id not in issued_ids:
            issued_ids.add(new_id)
            return jsonify({"relay_id": new_id})

# -------------------------------
# Socket.IO: On Connect
# -------------------------------
@socketio.on('connect')
def handle_connect():
    sid = request.sid

    # Generate a unique user_id
    while True:
        user_id = str(random.randint(1000, 9999))
        if user_id not in user_id_to_sid and user_id not in issued_ids:
            break

    user_id_to_sid[user_id] = sid
    sid_to_user_id[sid] = user_id
    issued_ids.add(user_id)

    emit('your_id', user_id, room=sid)
    print(f"✅ User connected: {user_id} (SID: {sid})")

# -------------------------------
# Socket.IO: Handle Private Message
# -------------------------------
@socketio.on('private_message')
def handle_private_message(data):
    to_id = data.get('to')
    message = data.get('message')
    from_id = sid_to_user_id.get(request.sid)

    to_sid = user_id_to_sid.get(to_id)
    if to_sid:
        emit('message', f"{from_id}: {message}", to=to_sid)
    else:
        emit('message', f"User {to_id} is not online.", room=request.sid)

# -------------------------------
# Socket.IO: On Disconnect
# -------------------------------
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    user_id = sid_to_user_id.pop(sid, None)
    if user_id:
        user_id_to_sid.pop(user_id, None)
        issued_ids.discard(user_id)
        print(f"❌ User disconnected: {user_id}")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    print(f"🚀 Starting Private Chat Server on port {port}...")
    socketio.run(app, host='0.0.0.0', port=port)
