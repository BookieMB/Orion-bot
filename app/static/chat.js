document.addEventListener("DOMContentLoaded", () => {
    const chatList = document.getElementById("chat-list");
    const messagesDiv = document.getElementById("messages");
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const newChatBtn = document.getElementById("new-chat");
    const darkModeToggle = document.getElementById("dark-mode-toggle");

    let chats = [];
    let currentChatId = null;

    // Disable browser auto-suggest
    messageInput.setAttribute("autocomplete", "off");

    // Restore Dark Mode Preference
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark");
    }

    // Load chat history
    fetch("/chat/history")
        .then(res => res.json())
        .then(data => {
            chats = data.history.map((msg, idx) => ({
                id: idx + 1,
                title: msg.content.slice(0, 20) || "Untitled Chat",
                messages: [msg]
            }));
            renderChatList();
        });

    function renderChatList() {
        chatList.innerHTML = "";
        chats.forEach(chat => {
            const li = document.createElement("li");
            li.dataset.id = chat.id;

            // Title span (to keep delete button separate)
            const titleSpan = document.createElement("span");
            titleSpan.textContent = chat.title;
            titleSpan.className = "chat-title";
            li.appendChild(titleSpan);

            // Rename on double click
            titleSpan.addEventListener("dblclick", () => {
                const input = document.createElement("input");
                input.type = "text";
                input.value = chat.title;
                input.className = "rename-input";
                titleSpan.replaceWith(input);
                input.focus();

                input.addEventListener("blur", save);
                input.addEventListener("keydown", e => {
                    if (e.key === "Enter") save();
                });

                function save() {
                    chat.title = input.value.trim() || "Untitled Chat";
                    renderChatList();
                }
            });

            // Delete button
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "x";
            deleteBtn.className = "delete-chat";
            deleteBtn.addEventListener("click", (e) => {
                e.stopPropagation(); // prevent loading the chat
                chats = chats.filter(c => c.id !== chat.id);
                if (currentChatId === chat.id) {
                    currentChatId = null;
                    messagesDiv.innerHTML = "";
                }
                renderChatList();
            });

            li.appendChild(deleteBtn);

            // Load chat on click
            li.addEventListener("click", () => loadChat(chat.id));
            chatList.appendChild(li);
        });
    }

    function loadChat(id) {
        const chat = chats.find(c => c.id === id);
        if (!chat) return;
        currentChatId = id;
        messagesDiv.innerHTML = "";
        chat.messages.forEach(m => addMessage(m.role, m.content));
    }

    function addMessage(role, content) {
        const msg = document.createElement("div");
        msg.classList.add("message", role);
        msg.textContent = content;
        messagesDiv.appendChild(msg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function showThinkingEffect() {
        const thinking = document.createElement("div");
        thinking.classList.add("message", "assistant", "thinking");
        thinking.textContent = "Orion is thinking";
        messagesDiv.appendChild(thinking);

        let dots = 0;
        const interval = setInterval(() => {
            dots = (dots + 1) % 4;
            thinking.textContent = "Thinking" + ".".repeat(dots);
        }, 500);

        return () => {
            clearInterval(interval);
            thinking.remove();
        };
    }

    chatForm.addEventListener("submit", e => {
        e.preventDefault();
        const content = messageInput.value.trim();
        if (!content) return;
        messageInput.value = "";

        addMessage("user", content);

        if (!currentChatId) {
            currentChatId = chats.length + 1;
            chats.push({ id: currentChatId, title: content.slice(0, 20), messages: [] });
            renderChatList();
        }

        const chat = chats.find(c => c.id === currentChatId);
        chat.messages.push({ role: "user", content });

        const stopThinking = showThinkingEffect();

        fetch("/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: content })
        })
            .then(res => res.json())
            .then(data => {
                stopThinking();
                addMessage("assistant", data.content);
                chat.messages.push({ role: "assistant", content: data.content });
            })
            .catch(err => {
                stopThinking();
                addMessage("assistant", "Error: " + err.message);
            });
    });

    newChatBtn.addEventListener("click", () => {
        currentChatId = null;
        messagesDiv.innerHTML = "";
    });

    // Dark Mode Toggle with Persistence
    darkModeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        localStorage.setItem("darkMode", document.body.classList.contains("dark"));
    });
});

function deleteChat(chatId) {
    fetch(`/chat/history/${chatId}`, { method: "DELETE" })
        .then(res => {
            if (res.ok) {
                // Remove from UI
                document.querySelector(`#chat-${chatId}`).remove();
            }
        });
}
