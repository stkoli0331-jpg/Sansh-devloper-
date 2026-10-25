import streamlit as st

st.set_page_config(page_title="Sansh Studio", page_icon="🎨", layout="wide")

st.title("🎨 Sansh Studio & Control Hub")
st.markdown("Yahan par saari themes, custom color pickers, aur wallet/credits manage honge.")

# Theme Settings
st.subheader("⚙️ Theme Customization")
theme_mode = st.selectbox("Choose Theme Mode:", ["Light Mode (Claude Orange)", "Dark Mode (Neon Green)"])

if theme_mode == "Light Mode (Claude Orange)":
    st.info("Claude Orange Light Mode is active.")
else:
    st.success("Dark Mode (Neon Green) is active.")

# Wallet & Credits Section
st.markdown("---")
st.subheader("💼 Wallet & Credits System")
st.metric(label="Available User Credits", value="100 / 100")
st.write("Aage chal kar yahan sth subscriptions aur earnings track hongi.")

