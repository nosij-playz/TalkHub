// static/chat/chat.js

// Connect to server using global SERVER_URL defined in config.js
const socket = io(SERVER_URL, {
  transports: ['websocket'],
  path: '/socket.io'
});

let myId = null;
let partnerId = null;

// On connection
socket.on("connect", () => {
  console.log("✅ Connected to Talk Hub");
});

// Receive unique ID
socket.on("your_id", id => {
  myId = id;
  document.getElementById("myId").textContent = id;
});

// Receive message from server
socket.on("message", data => {
  let from = "Partner";
  let msg = "";

  // Parse incoming message format
  if (typeof data === "object") {
    from = data.from || "Unknown";
    msg = data.message || "";
  } else if (typeof data === "string" && data.includes(":")) {
    const parts = data.split(":", 2);
    from = parts[0].trim();
    msg = parts[1].trim();
  } else {
    msg = data;
  }

  // Assign partner ID if not set and not from self
  if (!partnerId && from !== "Unknown" && from !== myId) {
    partnerId = from;
    document.getElementById("partnerInput").value = partnerId;
    alert("🔗 Partner connected: " + partnerId);
  }

  if (from !== myId) {
    appendMessage("Partner", msg);
  }
});

// Append chat bubble
function appendMessage(sender, message) {
  const chatBox = document.getElementById("chatBox");
  const bubble = document.createElement("p");

  bubble.className = sender === "You" ? "from-user" : "from-partner";
  bubble.textContent = message;

  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Start chat by entering partner ID
function startChat() {
  const input = document.getElementById("partnerInput").value.trim();
  if (!input) {
    alert("❗ Enter a valid partner ID to start chat.");
    return;
  }
  partnerId = input;
  alert("💬 Chat started with: " + partnerId);
}

// Send message
function sendMessage() {
  const inputBox = document.getElementById("messageInput");
  const msg = inputBox.value.trim();
  const inputPartner = document.getElementById("partnerInput").value.trim();

  if (!msg || !inputPartner) {
    alert("⚠️ Enter both message and partner ID.");
    return;
  }

  partnerId = inputPartner;

  socket.emit("private_message", {
    to: partnerId,
    message: msg
  });

  appendMessage("You", msg);
  inputBox.value = "";
}
