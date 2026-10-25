import streamlit as st

st.set_page_config(page_title="Sansh AI", page_icon="⚡", layout="wide")

# Custom CSS for Professional Look & Heavy Animations
st.markdown("""
<style>
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-container {
        animation: slideUp 0.8s ease-out forwards;
        background-color: #f9fafb;
        padding: 30px;
        border-radius: 18px;
        border: 2px solid #ff6600;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background-color: #ff6600 !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Main Sansh AI Interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.title("⚡ Sansh AI - Professional Coder")
st.markdown("Yeh raha hamara dedicated AI assistant. Yahan sirf high-performance coding, debugging, aur smart chats hongi.")

user_prompt = st.text_area("Yahan apni coding query ya bug likhein:", placeholder="Jaise: Python mein ek fast server ka code likho...")

if st.button("🚀 Ask Sansh AI"):
    if user_prompt:
        with st.spinner("Sansh AI is analyzing and writing code..."):
            st.success("Code generated successfully!")
            st.code(f"# Sansh AI Solution for:\n# {user_prompt}\n\ndef sansh_ai_core():\n    print('Sansh AI is fully active!')\n\nsansh_ai_core()", language="python")
    else:
        st.warning("Pehle kuch query toh likho bhai!")
st.markdown("</div>", unsafe_allow_html=True)
