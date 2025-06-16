class Chatbot {
  constructor() {
    this.isOpen = false;
    this.messages = [];
    this.isTyping = false;

    // DOM elements
    this.chatbot = document.querySelector(".chatbot");
    this.trigger = document.querySelector(".chatbot__button");
    this.closeBtn = document.querySelector(".chatbot__close");
    this.input = document.querySelector(".chatbot__input");
    this.sendBtn = document.querySelector(".chatbot__send");
    this.messagesContainer = document.querySelector(".chatbot__messages");

    this.init();
  }

  init() {
    // Event listeners
    this.trigger.addEventListener("click", () => this.toggleChat());
    this.closeBtn.addEventListener("click", () => this.closeChat());
    this.sendBtn.addEventListener("click", () => this.sendMessage());

    // Enter key to send message
    this.input.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Input validation
    this.input.addEventListener("input", () => {
      this.updateSendButton();
    });

    // Initialize send button state
    this.updateSendButton();
  }

  toggleChat() {
    if (this.isOpen) {
      this.closeChat();
    } else {
      this.openChat();
    }
  }

  openChat() {
    this.isOpen = true;
    this.chatbot.classList.add("chatbot--active");

    // Add body class for mobile full-screen
    if (window.innerWidth <= 768) {
      document.body.classList.add("chatbot-open");
    }

    this.input.focus();
  }

  closeChat() {
    this.isOpen = false;
    this.chatbot.classList.remove("chatbot--active");

    // Remove body class for mobile full-screen
    document.body.classList.remove("chatbot-open");
  }

  updateSendButton() {
    const hasText = this.input.value.trim().length > 0;
    this.sendBtn.disabled = !hasText || this.isTyping;
  }

  sendMessage() {
    const text = this.input.value.trim();
    if (!text || this.isTyping) return;

    // Add user message
    this.addMessage(text, "user");
    this.input.value = "";
    this.updateSendButton();

    // Send to backend
    this.sendToBackend(text);
  }

  addMessage(text, sender) {
    const messageElement = document.createElement("div");
    messageElement.className = `message message--${sender}`;

    // Add initial state for animation
    messageElement.style.opacity = "0";
    messageElement.style.transform =
      sender === "user" ? "translateX(30px)" : "translateX(-30px)";

    if (sender === "bot") {
      const avatar = document.createElement("div");
      avatar.className = "message__avatar";
      avatar.innerHTML =
        '<img src="/static/images/88hours-logo.svg" alt="Avatar" />';
      messageElement.appendChild(avatar);
    }

    const content = document.createElement("div");
    content.className = "message__content";

    const bubble = document.createElement("div");
    bubble.className = "message__bubble";
    bubble.textContent = text;

    content.appendChild(bubble);
    messageElement.appendChild(content);

    // Remove typing indicator if present
    this.removeTypingIndicator();

    // Add message to container
    this.messagesContainer.appendChild(messageElement);

    // Trigger animation
    requestAnimationFrame(() => {
      messageElement.style.opacity = "1";
      messageElement.style.transform = "translateX(0)";
      messageElement.style.transition = "all 0.4s ease-out";
    });

    this.scrollToBottomSmooth();

    // Store message
    this.messages.push({ text, sender, timestamp: new Date() });
  }

  sendToBackend(userMessage) {
    this.isTyping = true;
    this.updateSendButton();
    this.showTypingIndicator();

    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    })
      .then((response) => response.json())
      .then((data) => {
        this.addMessage(data.answer, "bot");
        this.isTyping = false;
        this.updateSendButton();
      })
      .catch((error) => {
        console.error("Error:", error);
        this.addMessage(
          "Sorry, I'm having trouble connecting. Please try again.",
          "bot"
        );
        this.isTyping = false;
        this.updateSendButton();
      });
  }

  showTypingIndicator() {
    const typingElement = document.createElement("div");
    typingElement.className = "message message--bot typing-message";
    typingElement.style.opacity = "0";
    typingElement.style.transform = "translateX(-30px)";

    typingElement.innerHTML = `
          <div class="message__avatar">
              <img src="/static/images/88hours-logo.svg" alt="Bot" />
          </div>
          <div class="message__content">
              <div class="message__bubble">
                  <div class="typing-indicator">
                      <div class="typing-dot"></div>
                      <div class="typing-dot"></div>
                      <div class="typing-dot"></div>
                  </div>
              </div>
          </div>
      `;

    this.messagesContainer.appendChild(typingElement);

    // Animate in
    requestAnimationFrame(() => {
      typingElement.style.opacity = "1";
      typingElement.style.transform = "translateX(0)";
      typingElement.style.transition = "all 0.3s ease-out";
    });

    this.scrollToBottomSmooth();
  }

  removeTypingIndicator() {
    const typingMessage =
      this.messagesContainer.querySelector(".typing-message");
    if (typingMessage) {
      typingMessage.remove();
    }
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  scrollToBottomSmooth() {
    this.messagesContainer.scrollTo({
      top: this.messagesContainer.scrollHeight,
      behavior: "smooth",
    });
  }
}

// Initialize chatbot when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new Chatbot();
});
