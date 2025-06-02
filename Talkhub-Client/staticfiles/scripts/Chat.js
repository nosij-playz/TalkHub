let lastHtml = '';

function fetchMessages() {
  const historyBox = document.querySelector(".chat-history");
  if (!historyBox) return;

  const userId = historyBox.dataset.userId;
  if (!userId) return;

  fetch(`/chat/messages/${userId}/`)
    .then(res => res.text())
    .then(html => {
      if (html !== lastHtml) {
        historyBox.innerHTML = html;
        historyBox.scrollTop = historyBox.scrollHeight;
        lastHtml = html;
      }
    });
}

setInterval(fetchMessages, 2000);
