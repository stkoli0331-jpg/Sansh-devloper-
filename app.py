import streamlit as st
import time

st.set_page_config(page_title="Santosh AI", page_icon="⚡", layout="centered")

# Hide default headers & footers for native app feel
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    body, .stApp {
        background-color: #f7f6f2; /* Minimalist cream tone matching logo background */
        color: #1a1a1a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Pulsing & Fade-in Animation for Splash Screen */
    @keyframes logoPulse {
        0% { transform: scale(0.92); opacity: 0.7; }
        50% { transform: scale(1.03); opacity: 1; filter: drop-shadow(0 0 12px rgba(217, 103, 56, 0.3)); }
        100% { transform: scale(1); opacity: 1; }
    }

    .splash-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 75vh;
        animation: logoPulse 2.2s ease-in-out infinite alternate;
    }

    .splash-brand {
        font-family: 'Georgia', serif;
        font-size: 28px;
        color: #d96738; /* Terracotta Orange matching logo */
        margin-top: 15px;
        font-weight: 500;
        letter-spacing: 1px;
    }

    .splash-footer {
        position: fixed;
        bottom: 40px;
        width: 100%;
        text-align: center;
        font-family: 'Georgia', serif;
        font-size: 14px;
        letter-spacing: 2px;
        color: #666666;
        text-transform: uppercase;
    }

    /* Landing Screen Header Styling */
    .app-header {
        text-align: center;
        margin-top: 50px;
        margin-bottom: 30px;
    }

    .user-greeting {
        font-family: 'Georgia', serif;
        font-size: 32px;
        color: #2b2b2b;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mock user login state (Tujhe badalne ke liye: st.session_state.user_name = "Mohit")
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mohit"  # Set to None if not logged in

# -----------------------------------------------------------------------------
# 1. LAUNCH / SPLASH SCREEN ANIMATION PHASE
# -----------------------------------------------------------------------------
if not st.session_state.splash_done:
    splash_placeholder = st.empty()
    with splash_placeholder.container():
        st.markdown("""
            <div class="splash-container">
                <!-- SVG Icon replicating your starburst design -->
                <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="4" fill="#d96738"/>
                    <path d="M50 10 L50 90 M10 50 L90 50 M22 22 L78 78 M22 78 L78 22" stroke="#2b2b2b" stroke-width="2" stroke-linecap="round"/>
                    <path d="M50 25 L50 75 M25 50 L75 50" stroke="#d96738" stroke-width="3" stroke-linecap="round"/>
                </svg>
                <div class="splash-brand">Sansh</div>
            </div>
            <div class="splash-footer">Santosh</div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)  # Animation Duration
    
    st.session_state.splash_done = True
    st.rerun()

# -----------------------------------------------------------------------------
# 2. MAIN APP INTERFACE PHASE
# -----------------------------------------------------------------------------

# Dynamic Header depending on Login State
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
            <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M50 10 L50 90 M10 50 L90 50 M22 22 L78 78 M22 78 L78 22" stroke="#2b2b2b" stroke-width="3"/>
                <path d="M50 25 L50 75 M25 50 L75 50" stroke="#d96738" stroke-width="4"/>
            </svg>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("user_name"):
        st.markdown(f"<h2 class='user-greeting' style='text-align: center;'>{st.session_state.user_name}</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 class='user-greeting' style='text-align: center;'>Santosh chat?</h2>", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Bottom Fixed Chat Bar
if prompt := st.chat_input("Message Santosh..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = f"Santosh AI Response to: '{prompt}'"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()
    
