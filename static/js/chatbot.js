class Chatbot {
    constructor() {
        this.isOpen = false;
        this.init();
    }

    init() {
        this.createChatbotUI();
        this.attachEventListeners();
    }

    createChatbotUI() {
        const chatbotHTML = `
            <div id="chatbot-container" class="chatbot-container">
                <button id="chatbot-toggle" class="chatbot-toggle" title="AI 챗봇">
                    ?
                </button>
                <div id="chatbot-window" class="chatbot-window" style="display: none;">
                    <div class="chatbot-header">
                        <h3>AI 번역 도우미</h3>
                        <button id="chatbot-close" class="chatbot-close">✕</button>
                    </div>
                    <div id="chatbot-messages" class="chatbot-messages">
                        <div class="chatbot-message bot-message">
                            안녕하세요! AI 번역 도우미입니다.<br>
                            번역, 언어 학습, 문법 체크 등 무엇이든 물어보세요.
                        </div>
                    </div>
                    <div class="chatbot-input-area">
                        <input 
                            type="text" 
                            id="chatbot-input" 
                            placeholder="질문을 입력하세요..."
                            autocomplete="off"
                        >
                        <button id="chatbot-send">전송</button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    attachEventListeners() {
        document.getElementById('chatbot-toggle').addEventListener('click', () => this.toggle());
        document.getElementById('chatbot-close').addEventListener('click', () => this.close());
        document.getElementById('chatbot-send').addEventListener('click', () => this.sendMessage());
        document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    toggle() {
        this.isOpen = !this.isOpen;
        const window = document.getElementById('chatbot-window');
        window.style.display = this.isOpen ? 'flex' : 'none';
        if (this.isOpen) {
            document.getElementById('chatbot-input').focus();
        }
    }

    close() {
        this.isOpen = false;
        document.getElementById('chatbot-window').style.display = 'none';
    }

    sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message) return;

        this.addMessage(message, 'user');
        input.value = '';

        this.getAIResponse(message);
    }

    async getAIResponse(message) {
        this.addMessage('...', 'bot-typing');
        
        try {
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            const typingMsg = document.querySelector('.bot-typing');
            if (typingMsg) typingMsg.remove();
            
            if (data.response) {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage('응답을 받지 못했습니다.', 'bot');
            }
        } catch (error) {
            const typingMsg = document.querySelector('.bot-typing');
            if (typingMsg) typingMsg.remove();
            this.addMessage('오류가 발생했습니다. 다시 시도해주세요.', 'bot');
        }
    }

    addMessage(text, type) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${type}-message`;
        if (type === 'bot-typing') {
            messageDiv.classList.add('bot-typing');
        }
        messageDiv.innerHTML = text.replace(/\n/g, '<br>');
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}

let chatbot;

document.addEventListener('DOMContentLoaded', () => {
    chatbot = new Chatbot();
});
