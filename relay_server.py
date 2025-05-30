from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

clients = set()

@app.route('/')
def index():
    return {"message": "WebSocket Relay Server is Running!"}

@socketio.on('connect')
def handle_connect():
    clients.add(request.sid)
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    clients.discard(request.sid)
    print(f"Client disconnected: {request.sid}")

@socketio.on('message')
def handle_message(msg):
    print(f"Message from {request.sid}: {msg}")
    # Relay to all clients except the sender
    for client in clients:
        if client != request.sid:
            socketio.emit('message', msg, room=client)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
