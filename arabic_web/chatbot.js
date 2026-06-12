// chatbot.js

document.addEventListener("DOMContentLoaded", function () {
    // 1. Create HTML structure dynamically
    const chatHTML = `
        <button id="chatBtn" class="chat-btn">💬</button>
        <div id="chatWindow" class="chat-window" dir="rtl">
            <div class="chat-header">
                <span>مساعدك الهندسي الذكي</span>
                <button id="closeChatBtn" class="chat-close">×</button>
            </div>
            <div id="chatBody" class="chat-body">
                <div class="message bot-msg">مرحباً بك! أنا مهندس كهرباء قوى. كيف يمكنني مساعدتك اليوم؟</div>
            </div>
            <div class="chat-footer">
                <input type="text" id="chatInput" class="chat-input" placeholder="اكتب سؤالك هنا..." />
                <button id="chatSendBtn" class="chat-send-btn">إرسال <span id="timerText" class="timer-text"></span></button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', chatHTML);

    // 2. Select elements
    const chatBtn = document.getElementById('chatBtn');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatWindow = document.getElementById('chatWindow');
    const chatBody = document.getElementById('chatBody');
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const timerText = document.getElementById('timerText');

    // 3. Configuration
    const COOLDOWN_SECONDS = 15; // 15 seconds to prevent rate limit
    let isOnCooldown = false;
    // Update this URL if your Python server is hosted elsewhere
    const API_URL = "http://localhost:5000/api/chat";

    // 4. Toggle Window
    chatBtn.addEventListener('click', () => {
        chatWindow.classList.add('active');
        chatBtn.style.display = 'none';
    });

    closeChatBtn.addEventListener('click', () => {
        chatWindow.classList.remove('active');
        chatBtn.style.display = 'block';
    });

    // 5. Send Message Logic
    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text || isOnCooldown) return;

        // Add User Message to UI
        addMessage(text, 'user-msg');
        chatInput.value = '';

        // Start Cooldown Timer
        startCooldown();

        // Add Loading Bot Message
        const loadingId = addMessage('جاري التفكير...', 'bot-msg');

        try {
            // Send to Backend
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            
            // Remove loading and add real response
            removeMessage(loadingId);
            if (data.response) {
                addMessage(data.response, 'bot-msg');
            } else {
                addMessage('عذراً، حدث خطأ. ' + (data.error || ''), 'bot-msg');
            }
        } catch (error) {
            removeMessage(loadingId);
            addMessage('تعذر الاتصال بالخادم. تأكد من تشغيل chat_server.py.', 'bot-msg');
            console.error('Chat Error:', error);
        }
    }

    // 6. UI Helpers
    function addMessage(text, className) {
        const id = 'msg-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${className}`;
        msgDiv.id = id;
        
        // Simple markdown parsing for bold text if gemini returns markdown
        let formattedText = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
        formattedText = formattedText.replace(/\\n/g, '<br>');
        
        msgDiv.innerHTML = formattedText;
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll
        return id;
    }

    function removeMessage(id) {
        const msgDiv = document.getElementById(id);
        if (msgDiv) msgDiv.remove();
    }

    // 7. Cooldown Timer Logic
    function startCooldown() {
        isOnCooldown = true;
        chatSendBtn.disabled = true;
        chatInput.disabled = true;
        chatInput.placeholder = "انتظر قليلاً...";
        
        let timeLeft = COOLDOWN_SECONDS;
        timerText.textContent = `(${timeLeft})`;

        const timer = setInterval(() => {
            timeLeft--;
            if (timeLeft <= 0) {
                clearInterval(timer);
                isOnCooldown = false;
                chatSendBtn.disabled = false;
                chatInput.disabled = false;
                chatInput.placeholder = "اكتب سؤالك هنا...";
                timerText.textContent = '';
                chatInput.focus();
            } else {
                timerText.textContent = `(${timeLeft})`;
            }
        }, 1000);
    }

    // 8. Event Listeners
    chatSendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
