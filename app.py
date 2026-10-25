import streamlit as st

st.set_page_config(page_title="Sansh AI", page_icon="⚡", layout="centered")

# Clean, Professional Mobile-First Styling
st.markdown("""
<style>
    /* Main background & smooth fonts */
    .stApp {
        background-color: #fafafa;
    }
    
    /* Clean Text Area */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 12px !important;
        font-size: 15px !important;
    }
    .stTextArea textarea:focus {
        border-color: #ff6600 !important;
        box-shadow: 0 0 0 2px rgba(255, 102, 0, 0.2) !important;
    }

    /* Modern Gradient Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff6600, #ff8533) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(255, 102, 0, 0.35);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(255, 102, 0, 0.45);
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("## ⚡ Sansh AI")
st.markdown("<p style='color: #64748b; font-size: 14px; margin-top: -10px;'>High-Performance Professional Coder & Assistant</p>", unsafe_allow_html=True)
st.markdown("---")

# Main Interface
user_prompt = st.text_area("💬 Apna coding sawal ya bug yahan likhein:", placeholder="Jaise: Python mein ek fast API ka code likho...", height=130)

st.write("") # Thoda space dene ke liye

if st.button("🚀 Ask Sansh AI"):
    if user_prompt:
        with st.spinner("Sansh AI is writing code..."):
            st.success("Code Generated Successfully!")
            st.code(f"# Sansh AI Solution for:\n# {user_prompt}\n\ndef sansh_core():\n    print('Hello from Sansh AI!')\n\nsansh_core()", language="python")
    else:
        st.warning("Pehle kuch query toh likho bhai!")
        
