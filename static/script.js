const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

function getTime() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage(text, sender, typing = false) {
  const msg = document.createElement("div");
  msg.classList.add("msg", sender);

  if (typing) msg.classList.add("typing");

  msg.innerHTML = `
    <div>${text}</div>
    <span class="time">${getTime()}</span>
  `;

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;

  return msg;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";

  // typing indicator
  const typingMsg = addMessage("Bot is typing...", "bot", true);

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message }),
  });

  const data = await response.json();

  // remove typing indicator
  typingMsg.remove();

  addMessage(data.reply, "bot");
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

clearBtn.addEventListener("click", function () {
  chatBox.innerHTML = "";
  addMessage("Hello! How are you feeling today?", "bot");
});

// First message
addMessage("Hello! How are you feeling today?", "bot");
