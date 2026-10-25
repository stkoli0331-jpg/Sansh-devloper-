import streamlit as st

st.set_page_config(page_title="Sansh AI", page_icon="⚡", layout="wide")

# Custom CSS for Animations & Claude Light/Dark Theme
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-card {
        animation: fadeIn 0.7s ease-out forwards;
        background-color: #f9fafb;
        padding: 25px;
        border-radius: 16px;
        border: 2px solid #ff6600;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    }
    .stButton>button {
        background-color: #ff6600 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
    }
</style>
""", unsafe_allow_html=True)

# Main Sansh AI Chat Interface
st.markdown("<div class='chat-card'>", unsafe_allow_html=True)
st.title("⚡ Sansh AI - Professional Coder")
st.markdown("Yeh raha hamara main AI assistant. Yahan tu apna code likh, bug fix karwa ya koi bhi technical sawal pooch.")

user_input = st.text_area("Apna coding sawal yahan likhein:", placeholder="Jaise: Write a Python script...")

if st.button("🚀 Ask Sansh AI"):
    if user_input:
        with st.spinner("Sansh AI is writing code..."):
            st.success("Code generated successfully!")
            st.code(f"# Sansh AI Output for:\n# {user_input}\n\nprint('Hello from Sansh AI!')", language="python")
    else:
        st.warning("Pehle kuch query toh likho bhai!")
st.markdown("</div>", unsafe_allow_html=True)

