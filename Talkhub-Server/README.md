
# 🔌 Talkhub Server – Flask Socket.IO Relay

This is the **Flask + Socket.IO-based relay server** for the Talkhub chat application. It handles real-time messaging.

---

## 📁 Folder Structure

```
Talkhub-Server/
└── server.py
```

---

## ⚙️ How It Works

- Runs a **Socket.IO server** for real-time communication.
- Accepts `private_message` events and forwards them to the appropriate recipient using their `relay_id`.
- Keeps track of connected clients.

---

## ▶️ Run Server

```bash
cd Talkhub-Server
python server.py
```

Runs on: `http://0.0.0.0:5000/` or the host assigned by any subdomain platform (e.g. https://talkhub-server.onrender.com)

---

## 🧠 Responsibilities

- No data storage
- Stateless message relay
- Works only as a real-time socket message bridge

Make sure this server is running before launching the Django client.

---

## 🖼️ Screenshots

Screenshots demonstrating the UI are available in the `Pics/` folder:
- `7.png` and `8.png`: Show server responses and backend relay operations.

### Preview

| ![](Pics/7.png) | ![](Pics/8.png) |                 |
