import streamlit as st

# Page Configuration
st.set_page_config(page_title="Sansh AI", page_icon="⚡", layout="wide")

# Sidebar - Ultimate Theme & Customization Studio
st.sidebar.title("🎨 Sansh AI Theme Studio")
theme_choice = st.sidebar.radio(
    "Theme Mode Choose Karein:", 
    [
        "Light Mode (Claude Orange - Default)", 
        "Dark Mode (Neon Green)", 
        "Custom Color Picker 🎨"
    ]
)

# Theme Logic & Default Colors
if theme_choice == "Light Mode (Claude Orange - Default)":
    bg_color = "#ffffff"
    text_color = "#1f2937"
    card_bg = "#f9fafb"
    accent_color = "#ff6600"  # Claude Orange
    border_color = "#ff6600"
elif theme_choice == "Dark Mode (Neon Green)":
    bg_color = "#0e1117"
    text_color = "#ffffff"
    card_bg = "#161b22"
    accent_color = "#00ff66"  # Neon Green
    border_color = "#00ff66"
else:
    # Custom User Choice via Color Picker
    bg_color = st.sidebar.color_picker("Background Color", "#0e1117")
    text_color = st.sidebar.color_picker("Text Color", "#ffffff")
    card_bg = st.sidebar.color_picker("Card Background Color", "#161b22")
    accent_color = st.sidebar.color_picker("Accent & Icon Color", "#ff6600")
    border_color = accent_color

# Custom CSS with Heavy Animations Everywhere
css_styles = f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: all 0.5s ease-in-out;
    }}
    
    /* Smooth Slide-Up Fade Animation */
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(25px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Heavy Glowing Pulse Animation on Hover */
    @keyframes pulseGlow {{
        0% {{ box-shadow: 0 0 5px {accent_color}; }}
        50% {{ box-shadow: 0 0 22px {accent_color}; }}
        100% {{ box-shadow: 0 0 5px {accent_color}; }}
    }}

    .animated-box {{
        animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        background-color: {card_bg};
        padding: 24px;
        border-radius: 18px;
        border: 2px solid {border_color};
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}

    .animated-box:hover {{
        animation: pulseGlow 2s infinite;
        transform: translateY(-4px);
    }}

    /* Custom Animated Buttons with Glowing Effect */
    .stButton>button {{
        background-color: {accent_color} !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 14px 28px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stButton>button:hover {{
        transform: scale(1.08) rotate(1deg);
        opacity: 0.95;
        box-shadow: 0 10px 25px {accent_color};
    }}

    /* Success Green Box with Animation */
    .success-box {{
        animation: slideUp 0.6s ease forwards;
        background-color: rgba(0, 255, 102, 0.15);
        border-left: 6px solid #00ff66;
        padding: 18px;
        border-radius: 10px;
        margin-top: 15px;
        color: {text_color};
    }}

    /* Error Red Box with Animation */
    .error-box {{
        animation: slideUp 0.6s ease forwards;
        background-color: rgba(255, 75, 75, 0.15);
        border-left: 6px solid #ff4b4b;
        padding: 18px;
        border-radius: 10px;
        margin-top: 15px;
        color: {text_color};
    }}
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# Main Header Container
st.markdown("<div class='animated-box'>", unsafe_allow_html=True)
st.title("⚡ Sansh AI - Pro Studio")
st.markdown("Default: **Light Mode + Claude Orange**, with full custom theme & heavy animations support!")
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar Wallet & Credits Info
st.sidebar.markdown("---")
st.sidebar.subheader("💼 Wallet & Credits")
st.sidebar.metric(label="Available Credits", value="100 / 100")
st.sidebar.success("✨ Custom theme switcher active!")

# Chat & Code Generator Section
st.markdown("<div class='animated-box'>", unsafe_allow_html=True)
st.subheader("💬 Code Generator & Bug Fixer")
user_prompt = st.text_area(
    "Yahan apni coding requirement ya error likhein:", 
    placeholder="Jaise: Python mein fast web app ka code likho..."
)

if st.button("🚀 Generate & Analyze Code"):
    if user_prompt:
        with st.spinner("Sansh AI is processing with smooth animations..."):
            # Success Green Box Output
            st.markdown(
                "<div class='success-box'>✅ <b>Success Box:</b> Code successfully generate ho gaya hai aur bilkul clean hai!</div>", 
                unsafe_allow_html=True
            )
            st.code(f"# Generated Code for: {user_prompt}\n\ndef sansh_ai_solution():\n    print('Sansh AI is running smoothly on mobile!')\n\nsansh_ai_solution()", language="python")
    else:
        # Error Red Box Output
        st.markdown(
            "<div class='error-box'>❌ <b>Error Box:</b> Bhai pehle kuch text ya prompt toh likh, khali button daba raha hai!</div>", 
            unsafe_allow_html=True
        )
st.markdown("</div>", unsafe_allow_html=True)
        
