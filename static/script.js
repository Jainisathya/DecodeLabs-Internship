function appendMessage(message, sender, timestamp) {
    const chatbox = document.getElementById("chatbox");

    const msgDiv = document.createElement("div");
    msgDiv.className = sender === "You" ? "user-message" : "bot-message";
    msgDiv.innerHTML = `
        <div>${message.replace(/\n/g, "<br>")}</div>
        <span class="timestamp">${timestamp}</span>
    `;

    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function loadHistory() {
    fetch("/history")
        .then(response => response.json())
        .then(history => {
            const historyPanel = document.getElementById("historyPanel");
            historyPanel.innerHTML = "";

            if (history.length === 0) {
                historyPanel.innerHTML = `<p class="empty-history">No chat history yet.</p>`;
                return;
            }

            history.forEach(chat => {
                const item = document.createElement("div");
                item.className = "history-item";
                item.innerHTML = `
                    <strong>${chat.sender}</strong>
                    <div>${chat.message.replace(/\n/g, "<br>")}</div>
                    <div class="history-time">${chat.timestamp}</div>
                `;
                historyPanel.appendChild(item);
            });

            historyPanel.scrollTop = historyPanel.scrollHeight;
        });
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const userInput = input.value.trim();

    if (userInput === "") return;

    // temporary user message
    appendMessage(userInput, "You", "Sending...");

    fetch("/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "msg=" + encodeURIComponent(userInput)
    })
    .then(response => response.json())
    .then(data => {
        // remove temporary "Sending..." message and redraw from history
        const chatbox = document.getElementById("chatbox");
        chatbox.innerHTML = `
            <div class="bot-message">
                <div>Hello! I am RuleBot. Ask me about AI, Python, date, time and more 😊</div>
                <span class="timestamp">Now</span>
            </div>
        `;

        loadChatWindow();
        loadHistory();
    });

    input.value = "";
}

function loadChatWindow() {
    fetch("/history")
        .then(response => response.json())
        .then(history => {
            const chatbox = document.getElementById("chatbox");

            chatbox.innerHTML = `
                <div class="bot-message">
                    <div>Hello! I am RuleBot. Ask me about AI, Python, date, time and more 😊</div>
                    <span class="timestamp">Now</span>
                </div>
            `;

            history.forEach(chat => {
                appendMessage(chat.message, chat.sender, chat.timestamp);
            });
        });
}

function clearHistory() {
    fetch("/clear", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("historyPanel").innerHTML =
            `<p class="empty-history">No chat history yet.</p>`;

        document.getElementById("chatbox").innerHTML = `
            <div class="bot-message">
                <div>Hello! I am RuleBot. Ask me about AI, Python, date, time and more 😊</div>
                <span class="timestamp">Now</span>
            </div>
        `;
    });
}

// Enter key support
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("userInput").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    loadHistory();
});