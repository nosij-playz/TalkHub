import socket
import threading

HOST = "x.tcp.ngrok.io"  # ← Replace with ngrok host from Colab
PORT = 12345             # ← Replace with ngrok port from Colab
BUFFER_SIZE = 1024

def receive(sock):
    while True:
        try:
            msg = sock.recv(BUFFER_SIZE).decode()
            if msg:
                print(msg)
        except:
            break

def send(sock):
    while True:
        try:
            msg = input()
            sock.send(msg.encode())
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    threading.Thread(target=receive, args=(client,), daemon=True).start()
    send(client)

if __name__ == "__main__":
    main()
