import streamlit as st
from auditor import SovereignAuditor
import os

# 1. Page Configuration
st.set_page_config(
    page_title="Sovereign Code Auditor", 
    page_icon="🛡️", 
    layout="centered"
)

# 2. Custom Styling for a "Fintech/Security" feel
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h3 { color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sovereign Code Auditor")
st.markdown("### Secure SLM-powered vulnerability scanning.")
st.divider()

# 3. Initialize Auditor with Error Handling
# This prevents the "Mistral import" or "API Key" issues from breaking the UI
if 'auditor' not in st.session_state:
    try:
        st.session_state.auditor = SovereignAuditor()
        st.success("✅ Audit Engine Active")
    except Exception as e:
        st.error(f"⚠️ Engine Offline: {e}")
        st.info("Check your .env file and ensure 'pip install mistralai>=1.0.0' was successful.")
        st.stop()

# 4. File Management
uploaded_files = st.file_uploader(
    "Upload Python (.py) or Ruby (.rb) files for deep analysis", 
    type=['py', 'rb'], 
    accept_multiple_files=True
)

# 5. Execution Logic
if st.button("🚀 Start Security Audit"):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Create a dynamic status container for each file
            with st.status(f"Scanning {uploaded_file.name}...", expanded=True) as status:
                try:
                    # Read and decode the file content locally
                    content = uploaded_file.read().decode("utf-8")
                    
                    st.write("🔍 Identifying logic patterns...")
                    
                    # Call the Mistral-powered agent
                    result = st.session_state.auditor.analyze_code(uploaded_file.name, content)
                    
                    # Display Results in a clean format
                    st.subheader(f"📋 Report: {uploaded_file.name}")
                    st.markdown(result)
                    
                    status.update(label=f"Audit Complete for {uploaded_file.name}!", state="complete")
                except Exception as file_err:
                    st.error(f"Error processing {uploaded_file.name}: {file_err}")
    else:
        st.warning("Please upload at least one file to begin.")

# 6. Sidebar Info
with st.sidebar:
    st.header("Security Metadata")
    st.info("""
    **Sovereign Logic:**
    - Local file parsing.
    - No training on your data.
    - Mistral SLM reasoning.
    """)
    if st.button("Clear Cache"):
        st.session_state.clear()
        st.rerun()