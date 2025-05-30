import eventlet
eventlet.monkey_patch()  # <- MUST be at the very top before any other imports

from flask import Flask, request
from flask_socketio import SocketIO, emit
import random
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

user_id_to_sid = {}
sid_to_user_id = {}

@app.route('/')
def index():
    return {"message": "Private Chat Server is Running!"}

@socketio.on('connect')
def handle_connect():
    user_id = str(random.randint(1000, 9999))
    sid = request.sid

    user_id_to_sid[user_id] = sid
    sid_to_user_id[sid] = user_id

    emit('your_id', user_id, room=sid)
    print(f"User connected: {user_id} (SID: {sid})")

@socketio.on('private_message')
def handle_private_message(data):
    to_id = data.get('to')
    message = data.get('message')
    from_id = sid_to_user_id.get(request.sid)

    to_sid = user_id_to_sid.get(to_id)

    if to_sid:
        emit('message', f"{from_id}: {message}", to=to_sid)
    else:
        emit('message', f"User {to_id} is not online.")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    user_id = sid_to_user_id.get(sid)
    if user_id:
        user_id_to_sid.pop(user_id, None)
        sid_to_user_id.pop(sid, None)
        print(f"User disconnected: {user_id}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
