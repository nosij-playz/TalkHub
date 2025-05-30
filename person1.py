import socketio
from config import SERVER_URL  # ✅ import predefined server URL

sio = socketio.Client()
my_id = None
partner_id = None

# === Event Handlers ===
@sio.event
def connect():
    print("🚀 Successfully connected to the server.")

@sio.on('your_id')
def receive_id(user_id):
    global my_id
    my_id = user_id
    print(f"🔑 Your unique ID is: {my_id}")
    ask_for_partner()

@sio.on('message')
def on_message(data):
    global partner_id

    if isinstance(data, dict):
        sender_id = data.get("from", "Unknown")
        msg = data.get("message", "")
    elif isinstance(data, str) and ":" in data:
        # Try to split message in format: "6569: message"
        parts = data.split(":", 1)
        sender_id = parts[0].strip()
        msg = parts[1].strip()
    else:
        # Fallback
        sender_id = "Unknown"
        msg = data

    if not partner_id and sender_id != "Unknown":
        partner_id = sender_id
        print(f"🔁 Chat partner set to {partner_id}")

    print(f"\n📩 {sender_id}: {msg}\nYou: ", end="")

@sio.event
def disconnect():
    print("❌ Disconnected from the server.")

@sio.event
def connect_error(data):
    print(f"❗ Connection failed: {data}")

# === Helper Functions ===

def ask_for_partner():
    global partner_id
    partner_id = input("👤 Enter the ID of the person you want to chat with (or leave empty to wait): ").strip()
    if partner_id:
        print("💬 You can now start chatting. Type 'exit' to quit.\n")
    else:
        print("⏳ Waiting for someone to message you...\n")
    chat_loop()

def chat_loop():
    while True:
        try:
            msg = input("You: ")
            if msg.lower() == 'exit':
                print("🔌 Disconnecting...")
                sio.disconnect()
                break
            if not partner_id or partner_id.lower() == "partner":
                print("⚠️ No valid partner ID yet. Please wait for someone to message you.")
                continue
            sio.emit('private_message', {"to": partner_id, "message": msg})
        except KeyboardInterrupt:
            print("\n🔌 Disconnecting...")
            sio.disconnect()
            break

# === Main ===

if __name__ == '__main__':
    try:
        sio.connect(
            SERVER_URL,
            transports=['websocket', 'polling'],
            socketio_path='/socket.io'
        )
        sio.wait()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
