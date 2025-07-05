import streamlit as st
from main import run_pipeline
import tempfile
import os

st.set_page_config(page_title="Soulful Alignment", layout="wide")

st.title("🧠 Soulful Alignment AI")
st.markdown("Reflect, critique, and revise your ideas with cultural insight and philosophical depth.")

user_input = st.text_area("💬 Enter your prompt:", height=200)

if st.button("Run Alignment"):
    if not user_input.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Running alignment pipeline..."):
            # Run the full pipeline
            run_pipeline(user_input)

        st.success("✅ Alignment complete. See the logs folder for output.")

        # Offer the newest log file for download
        logs = sorted([f for f in os.listdir("logs") if f.endswith(".md")])
        if logs:
            latest_log = logs[-1]
            with open(os.path.join("logs", latest_log), "rb") as f:
                st.download_button("📥 Download Markdown Output", f, file_name=latest_log, mime="text/markdown")
