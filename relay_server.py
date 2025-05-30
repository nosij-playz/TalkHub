from flask import Flask, jsonify
import socket
import threading

app = Flask(__name__)

# === Get system's current local IP ===
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable; just to get the local interface
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

CHAT_SERVER_IP = get_local_ip()
CHAT_SERVER_PORT = 6000

chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server.bind((CHAT_SERVER_IP, CHAT_SERVER_PORT))
chat_server.listen(2)

clients = []

def relay_messages(sender, receiver):
    while True:
        try:
            message = sender.recv(1024)
            if not message:
                break
            receiver.send(message)
        except:
            break
    sender.close()
    receiver.close()

def start_relay_server():
    print(f"Relay server listening on {CHAT_SERVER_IP}:{CHAT_SERVER_PORT}")
    while len(clients) < 2:
        client, addr = chat_server.accept()
        print(f"Client connected from {addr}")
        clients.append(client)

    c1, c2 = clients[0], clients[1]
    print("Two clients connected. Relaying messages...")
    threading.Thread(target=relay_messages, args=(c1, c2), daemon=True).start()
    threading.Thread(target=relay_messages, args=(c2, c1), daemon=True).start()

# Start the chat server in the background
threading.Thread(target=start_relay_server, daemon=True).start()

# === Flask Routes ===
@app.route('/')
def get_server_info():
    return jsonify({
        'message': 'Relay Server is Running!',
        'chat_server_ip': CHAT_SERVER_IP,
        'chat_server_port': CHAT_SERVER_PORT
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
