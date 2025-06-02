
# 🧩 Talkhub Client – Django Frontend & Logic Layer

This is the **Django-based frontend and logic layer** of the Talkhub chat application. It handles:

- User signup/login
- UI rendering
- Chat interface
- Message logging
- Relay ID management
- Interaction with MySQL database

---

## 📁 Folder Structure

```
Talkhub-Client/
├── accounts/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── utils.py
├── staticfiles/
├── Talkhub/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── middleware.py
├── manage.py
```

---

## ⚙️ How It Works

- **Users** log in or sign up with a unique 10-digit `userid`.
- On login, a **relay ID** is requested and stored.
- Chat interface allows real-time private messaging via a Socket.IO relay server.
- Chat messages are saved in a MySQL database.
- Online users are marked with a green dot.

---

## 🔗 Important URLs

**Relay Server URL (in `settings.py`):**
```python
RELAY_SERVER_URL = "yourserver url .com"
```

**Run Django Client:**
```bash
cd Talkhub-Client
python manage.py runserver
```

Then open: `http://127.0.0.1:8000/`

---

## 🗃️ Database Tables

- `User`: Registered users and credentials
- `Online`: Tracks currently online users and their relay IDs
- `History`: Message logs between users

---
## 🖼️ Screenshots

Screenshots demonstrating the UI are available in the `Pics/` folder:
- `1.png` to `6.png`: Cover login, signup, dashboard, online status, chat UI, etc.

### Preview

| ![](Pics/1.png) | ![](Pics/2.png) | ![](Pics/3.png) |
|-----------------|-----------------|-----------------|
| ![](Pics/4.png) | ![](Pics/5.png) | ![](Pics/6.png) |              |

---
