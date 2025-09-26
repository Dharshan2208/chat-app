let username = "";

document.getElementById("join").onclick = async () => {
  username = document.getElementById("username").value.trim();
  if (!username) return alert("Enter username");
  await fetch("/users/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username }),
  });
  loadMessages();
};

document.getElementById("send").onclick = sendMessage;
document.getElementById("message").addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const content = document.getElementById("message").value.trim();
  if (!content || !username) return;
  await fetch("/messages/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, content }),
  });
  document.getElementById("message").value = "";
  loadMessages();
}

async function loadMessages() {
  const res = await fetch("/messages/");
  const msgs = await res.json();
  const chat = document.getElementById("chat");
  chat.innerHTML = "";
  msgs.reverse().forEach((m) => {
    const div = document.createElement("div");
    div.classList.add("msg");
    div.classList.add(m.username === username ? "me" : "other");
    div.innerHTML = `<div>${m.username}: ${m.content}</div>
                        <div class="time">${new Date(
                          m.created_at
                        ).toLocaleTimeString()}</div>`;
    chat.appendChild(div);
  });
  chat.scrollTop = chat.scrollHeight;
}

setInterval(loadMessages, 2000);
