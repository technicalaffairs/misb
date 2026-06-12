// chatbot.js

document.addEventListener("DOMContentLoaded", function () {
    // 1. Create HTML structure dynamically
    const chatHTML = `
        <button id="chatBtn" class="chat-btn">💬</button>
        <div id="chatWindow" class="chat-window" dir="rtl">
            <div class="chat-header">
                <span>المساعد الهندسي الذكي</span>
                <button id="closeChatBtn" class="chat-close">×</button>
            </div>
            <div id="chatBody" class="chat-body">
                <div class="message bot-msg">مرحبا بك يا باشمهندس، كيف يمكنني مساعدتك اليوم؟</div>
            </div>
            <div class="chat-footer">
                <input type="text" id="chatInput" class="chat-input" placeholder="اسأل هنا..." />
                <button id="chatSendBtn" class="chat-send-btn">إرسال</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', chatHTML);

    const chatBtn = document.getElementById('chatBtn');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatWindow = document.getElementById('chatWindow');
    const chatBody = document.getElementById('chatBody');
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');

    // --- State Restoration ---
    const savedChat = sessionStorage.getItem('engChatHistory');
    if (savedChat) {
        chatBody.innerHTML = savedChat;
        // Clean orphaned loading
        const messages = chatBody.querySelectorAll('.message');
        messages.forEach(msg => {
            if (msg.textContent.includes('جاري التفكير...')) {
                msg.remove();
            }
        });
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    const savedState = sessionStorage.getItem('engChatState');
    if (savedState === 'open') {
        chatWindow.classList.add('active');
        chatBtn.style.display = 'none';
    }

    // --- API and Cooldown Logic ---
    const API_URL = 'http://127.0.0.1:5000/api/chat';
    const COOLDOWN_TIME = 15000; // 15 seconds for Cohere rate limits
    
    // Toggle Window
    chatBtn.addEventListener('click', () => {
        chatWindow.classList.add('active');
        chatBtn.style.display = 'none';
        sessionStorage.setItem('engChatState', 'open');
    });

    closeChatBtn.addEventListener('click', () => {
        chatWindow.classList.remove('active');
        chatBtn.style.display = 'block';
        sessionStorage.setItem('engChatState', 'closed');
    });

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Check cooldown
        const lastMsgTime = sessionStorage.getItem('lastMsgTime');
        if (lastMsgTime && Date.now() - parseInt(lastMsgTime) < COOLDOWN_TIME) {
            const remaining = Math.ceil((COOLDOWN_TIME - (Date.now() - parseInt(lastMsgTime))) / 1000);
            addMessage(`عذراً، يرجى الانتظار ${remaining} ثانية قبل إرسال سؤال جديد (لتفادي حظر الخادم).`, 'bot-msg');
            return;
        }

        addMessage(text, 'user-msg');
        chatInput.value = '';
        sessionStorage.setItem('lastMsgTime', Date.now().toString());

        const loadingId = addMessage('جاري التفكير...', 'bot-msg');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            removeMessage(loadingId);

            if (!response.ok) {
                throw new Error("Server Error");
            }

            const data = await response.json();
            if (data.error) {
                addMessage("حدث خطأ: " + data.error, 'bot-msg');
            } else {
                handleBotResponse(data.response);
            }

        } catch (error) {
            removeMessage(loadingId);
            addMessage('عذراً، حدث خطأ أثناء التواصل مع الذكاء الاصطناعي. تأكد من تشغيل الخادم (chat_server.py).', 'bot-msg');
            console.error(error);
        }
    }

    function handleBotResponse(text) {
        // Extract [OPEN_PAGE: path]
        const openPageRegex = /\[OPEN_PAGE:\s*(.+?)\]/g;
        let formattedText = text;
        let pagesToOpen = [];

        let match;
        while ((match = openPageRegex.exec(text)) !== null) {
            pagesToOpen.push(match[1]);
        }

        // Remove the tags from the text shown to the user
        formattedText = formattedText.replace(openPageRegex, '').trim();

        // Convert markdown links, bold, etc., to basic HTML
        formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formattedText = formattedText.replace(/\*(.*?)\*/g, '<em>$1</em>');
        formattedText = formattedText.replace(/\n/g, '<br>');

        addMessage(formattedText, 'bot-msg');

        // Dynamically open pages
        if (pagesToOpen.length > 0) {
            const rootUrl = getRootUrl();
            pagesToOpen.forEach(pagePath => {
                const fullUrl = rootUrl + pagePath.trim();
                setTimeout(() => {
                    window.open(fullUrl, '_blank');
                }, 500); // Small delay
            });
        }
    }

    function getRootUrl() {
        const currentUrl = window.location.href;
        const baseStr = "arabic_web/";
        const idx = currentUrl.indexOf(baseStr);
        if (idx !== -1) {
            return currentUrl.substring(0, idx); 
        }
        return window.location.origin + window.location.pathname.split("/arabic_web/")[0] + "/";
    }

    // UI Helpers
    function addMessage(text, className) {
        const id = 'msg-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${className}`;
        msgDiv.id = id;
        msgDiv.innerHTML = text; 
        
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight; 
        
        sessionStorage.setItem('engChatHistory', chatBody.innerHTML);
        return id;
    }

    function removeMessage(id) {
        const msgDiv = document.getElementById(id);
        if (msgDiv) {
            msgDiv.remove();
            sessionStorage.setItem('engChatHistory', chatBody.innerHTML);
        }
    }

    // Event Listeners
    chatSendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
