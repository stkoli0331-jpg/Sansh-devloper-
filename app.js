// Dynamic Time-based Greeting
const greetingEl = document.getElementById('greeting');
const hour = new Date().getHours();
let timeGreeting = "Good evening";

if (hour < 12) {
    timeGreeting = "Good morning";
} else if (hour < 17) {
    timeGreeting = "Good afternoon";
}

if (greetingEl) {
    greetingEl.textContent = `${timeGreeting}, Sansh`;
}

// Splash Screen Fade out effect
window.addEventListener('load', () => {
    const splash = document.getElementById('splash-screen');
    if (splash) {
        setTimeout(() => {
            splash.style.opacity = '0';
            setTimeout(() => {
                splash.style.display = 'none';
            }, 700);
        }, 1200);
    }
});
