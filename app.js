// App State Management (Checking User Login Session)
const AppState = {
    // Yahan hum check karenge ki user logged-in hai ya nahi
    // Tu ise true karke check kar sakta hai ya baad mein Gmail login API se connect kar dena
    user: {
        isLoggedIn: true, 
        name: "Mohit" // Agar Gmail ID ka naam Mohit hai toh yeh aayega
    },
    config: {
        splashDuration: 2500,
        guestGreeting: "Super AI chat?" // Guest ke liye normal text
    }
};

class SuperAIAppEngine {
    constructor() {
        this.init();
    }

    init() {
        this.renderGreeting();
        this.runLaunchSequence();
        this.bindEvents();
    }

    renderGreeting() {
        const greetingTarget = document.getElementById("greeting-text");
        if (!greetingTarget) return;

        // Dynamic condition: Agar logged in hai aur naam available hai, toh wahi naam dikhao
        if (AppState.user.isLoggedIn && AppState.user.name) {
            greetingTarget.textContent = AppState.user.name;
        } else {
            // Agar guest hai toh normal text show hoga
            greetingTarget.textContent = AppState.config.guestGreeting;
        }
    }

    runLaunchSequence() {
        setTimeout(() => {
            const splash = document.getElementById('splash-view');
            const mainApp = document.getElementById('main-view');

            splash.classList.add('splash-fade-out');
            setTimeout(() => {
                splash.style.display = 'none';
                mainApp.classList.remove('hidden');
                mainApp.classList.add('view-fade-in');
            }, 400);
        }, AppState.config.splashDuration);
    }

    bindEvents() {
        const sendBtn = document.getElementById('send-btn');
        const input = document.getElementById('chat-input');

        if (sendBtn && input) {
            sendBtn.addEventListener('click', () => this.sendMessage());
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        }
    }

    sendMessage() {
        const input = document.getElementById('chat-input');
        const text = input.value.trim();
        if (!text) return;

        input.value = '';
        document.getElementById('hero-section').style.display = 'none';

        const stream = document.getElementById('chat-stream');
        
        // User Message Bubble
        const userBubble = document.createElement('div');
        userBubble.className = 'self-end bg-[#e8e6df] text-[#1a1a1a] px-4 py-3 rounded-2xl max-w-[85%] mb-3 text-base';
        userBubble.textContent = text;
        stream.appendChild(userBubble);

        // AI Response Mock
        setTimeout(() => {
            const aiBubble = document.createElement('div');
            aiBubble.className = 'self-start text-[#1a1a1a] px-2 py-3 max-w-[90%] mb-3 text-base';
            aiBubble.textContent = `Super AI: Processing your request...`;
            stream.appendChild(aiBubble);
            stream.scrollTop = stream.scrollHeight;
        }, 500);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    window.app = new SuperAIAppEngine();
});
