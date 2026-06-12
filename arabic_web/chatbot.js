// chatbot.js

document.addEventListener("DOMContentLoaded", function () {
    // 1. Create HTML structure dynamically
    const chatHTML = `
        <button id="chatBtn" class="chat-btn">🔍</button>
        <div id="chatWindow" class="chat-window" dir="rtl">
            <div class="chat-header">
                <span>محرك البحث الذكي للمستندات</span>
                <button id="closeChatBtn" class="chat-close">×</button>
            </div>
            <div id="chatBody" class="chat-body">
                <div class="message bot-msg">مرحبا بك، اكتب اسم المعدة أو الإجراء الذي تبحث عنه وسأجد المستند فوراً!</div>
            </div>
            <div class="chat-footer">
                <input type="text" id="chatInput" class="chat-input" placeholder="ابحث هنا (مثال: عينة الزيت)..." />
                <button id="chatSendBtn" class="chat-send-btn">بحث</button>
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

    // --- State Restoration ---
    const savedChat = sessionStorage.getItem('engChatHistory');
    if (savedChat) {
        chatBody.innerHTML = savedChat;
        // Clean orphaned loading
        const messages = chatBody.querySelectorAll('.message');
        messages.forEach(msg => {
            if (msg.textContent.includes('جاري البحث...')) {
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

    // --- Global Search Index ---
    let searchIndex = null;
    let isFetching = false;

    // Helper: Determine root URL dynamically
    function getRootUrl() {
        const currentUrl = window.location.href;
        const baseStr = "arabic_web/";
        const idx = currentUrl.indexOf(baseStr);
        if (idx !== -1) {
            return currentUrl.substring(0, idx); // Returns URL up to the root (before arabic_web/)
        }
        // Fallback: try to guess based on standard paths
        return window.location.origin + window.location.pathname.split("/arabic_web/")[0] + "/";
    }

    const rootUrl = getRootUrl();
    const indexUrl = rootUrl + "search_index.json";

    // 4. Toggle Window
    chatBtn.addEventListener('click', () => {
        chatWindow.classList.add('active');
        chatBtn.style.display = 'none';
        sessionStorage.setItem('engChatState', 'open');
        
        // Pre-fetch index if not loaded
        if (!searchIndex && !isFetching) {
            fetchSearchIndex();
        }
    });

    closeChatBtn.addEventListener('click', () => {
        chatWindow.classList.remove('active');
        chatBtn.style.display = 'block';
        sessionStorage.setItem('engChatState', 'closed');
    });

    async function fetchSearchIndex() {
        isFetching = true;
        try {
            const response = await fetch(indexUrl);
            if (!response.ok) throw new Error("Network response was not ok");
            searchIndex = await response.json();
            console.log("Search index loaded successfully: " + searchIndex.length + " documents.");
        } catch (error) {
            console.error("Failed to fetch search index:", error);
        } finally {
            isFetching = false;
        }
    }

    // Simple Scoring Algorithm
    function calculateScore(item, keywords) {
        let score = 0;
        let content = (item.content || "").toLowerCase();
        let title = (item.title || "").toLowerCase();
        
        for (let kw of keywords) {
            if (title.includes(kw)) score += 10;
            if (content.includes(kw)) score += 1;
        }
        return score;
    }

    // 5. Send Message Logic
    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        addMessage(text, 'user-msg');
        chatInput.value = '';

        const loadingId = addMessage('جاري البحث...', 'bot-msg');

        // Ensure index is loaded
        if (!searchIndex) {
            if (!isFetching) fetchSearchIndex();
            // Wait until it's loaded
            while (isFetching) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        }

        removeMessage(loadingId);

        if (!searchIndex) {
            addMessage('عذراً، لم أتمكن من تحميل قاعدة بيانات المستندات.', 'bot-msg');
            return;
        }

        // Extract meaningful keywords
        let keywords = text.toLowerCase().split(/\s+/).filter(w => w.length > 2);
        
        // If nothing matches length filter, use the exact word
        if (keywords.length === 0) keywords.push(text.toLowerCase());

        let results = searchIndex.map(item => {
            return {
                item: item,
                score: calculateScore(item, keywords)
            };
        }).filter(res => res.score > 0);

        results.sort((a, b) => b.score - a.score);

        // Fallback for exact phrase matching if no scores hit
        if (results.length === 0) {
            const exactSearchStr = text.toLowerCase();
            results = searchIndex.filter(item => 
                (item.title && item.title.toLowerCase().includes(exactSearchStr)) ||
                (item.content && item.content.toLowerCase().includes(exactSearchStr))
            ).map(item => ({ item: item, score: 1 }));
        }

        if (results.length > 0) {
            const topResults = results.slice(0, 5); // Top 5 results
            let htmlReply = '<strong>لقد وجدت المستندات التالية التي قد تفيدك:</strong><br><ul style="margin-top: 10px; padding-right: 20px;">';
            
            topResults.forEach(res => {
                let linkHref = rootUrl + res.item.path;
                let title = res.item.title && res.item.title.trim() !== "" ? res.item.title : "مستند بدون عنوان";
                
                // If title is just a meaningless code or empty, try to derive from path
                if (title === "مستند بدون عنوان" || title === "") {
                    title = res.item.path.split('/').pop().replace('.htm', '').replace('.html', '');
                }

                htmlReply += `<li style="margin-bottom: 8px;"><a href="${linkHref}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold; border-bottom: 1px dashed #007bff;">${title}</a></li>`;
            });
            htmlReply += '</ul>';
            
            addMessage(htmlReply, 'bot-msg');
        } else {
            addMessage('عذراً، لم أتمكن من إيجاد أي مستندات تطابق بحثك. جرب استخدام كلمات أكثر عمومية.', 'bot-msg');
        }
    }

    // 6. UI Helpers
    function addMessage(text, className) {
        const id = 'msg-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${className}`;
        msgDiv.id = id;
        
        msgDiv.innerHTML = text; 
        
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll
        
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

    // 8. Event Listeners
    chatSendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
