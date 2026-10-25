import streamlit as st
import datetime

# Page Configuration
st.set_page_config(
    page_title="Sansh Developer Hub",
    page_icon="🚀",
    layout="wide"
)

# Custom Styling / Header
st.title("🚀 Sansh Developer Hub")
st.markdown("### *Built for High-Performance Engineering & Productivity*")
st.write("---")

# Sidebar Navigation
st.sidebar.title("Navigation Menu")
app_mode = st.sidebar.selectbox("Choose a Section", ["Dashboard", "Code Snippet Manager", "Task & Project Tracker", "System Info"])

# 1. Dashboard Section
if app_mode == "Dashboard":
    st.subheader("📊 Performance & Activity Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Project Status", value="Active", delta="Stable")
    with col2:
        st.metric(label="Code Quality", value="A+", delta="Optimized")
    with col3:
        st.metric(label="Deployment Readiness", value="100%", delta="Ready")
    
    st.info("💡 Tip: Use the sidebar to switch between different high-performance modules of this application.")

# 2. Code Snippet Manager Section
elif app_mode == "Code Snippet Manager":
    st.subheader("💻 Quick Code Snippet Vault")
    snippet_title = st.text_input("Snippet Title")
    snippet_code = st.text_area("Write or Paste your Code here:")
    
    if st.button("Save Snippet"):
        if snippet_title and snippet_code:
            st.success(f"Snippet '{snippet_title}' saved successfully!")
            st.code(snippet_code, language="python")
        else:
            st.warning("Please fill in both the title and code fields.")

# 3. Task & Project Tracker Section
elif app_mode == "Task & Project Tracker":
    st.subheader("🎯 Project Milestone Tracker")
    task_name = st.text_input("New Task Name")
    if st.button("Add Task"):
        if task_name:
            st.success(f"Task added: {task_name}")
        else:
            st.error("Task name cannot be empty.")
    
    st.write("Current Goals:")
    st.checkbox("Master Advanced Python & Data Structures")
    st.checkbox("Build Production-grade Web Apps")
    st.checkbox("Crack Microsoft SDE Roadmap")

# 4. System Info Section
elif app_mode == "System Info":
    st.subheader("⚙️ System Configuration")
    st.write(f"Current Date & Time: {datetime.datetime.now()}")
    st.write("Platform: Cloud-Native Streamlit Instance")
    st.success("All systems operating at peak efficiency.")

# Footer
st.write("---")
st.markdown("<p style='text-align: center;'>Developed with 🔥 by Sansh Developer</p>", unsafe_allow_html=True)
