// App State Control
const AppState = {
    // Current user context (Local storage or empty guest)
    user: {
        isLoggedIn: false, // Set false for Guest mode
        name: ""           // Dynamically filled if logged in
    },
    config: {
        splashDuration: 2200
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

    // Dynamic Time-Based Greeting
    getGreetingTimePrefix() {
        const hour = new Date().getHours();
        if (hour < 12) return "Good morning";
        if (hour < 17) return "Good afternoon";
        return "Good evening";
    }

    renderGreeting() {
        const greetingTarget = document.getElementById("greeting-text");
        if (!greetingTarget) return;

        const timePrefix = this.getGreetingTimePrefix();

        if (AppState.user.isLoggedIn && AppState.user.name) {
            greetingTarget.textContent = `${timePrefix}, ${AppState.user.name}`;
        } else {
            greetingTarget.textContent = `${timePrefix}`;
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
        const heroSection = document.getElementById('hero-section');
        if (heroSection) heroSection.style.display = 'none';

        const stream = document.getElementById('chat-stream');
        
        // User Bubble
        const userBubble = document.createElement('div');
        userBubble.className = 'self-end bg-[#e8e4db] text-[#1f1e1b] px-4 py-3 rounded-2xl max-w-[85%] mb-3 text-base';
        userBubble.textContent = text;
        stream.appendChild(userBubble);

        // AI Response Stream Placeholder
        setTimeout(() => {
            const aiBubble = document.createElement('div');
            aiBubble.className = 'self-start text-[#1f1e1b] px-2 py-3 max-w-[95%] mb-3 text-base';
            aiBubble.textContent = `Super AI: ${text} ke liye processing complete.`;
            stream.appendChild(aiBubble);
            stream.scrollTop = stream.scrollHeight;
        }, 400);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    window.app = new SuperAIAppEngine();
});

