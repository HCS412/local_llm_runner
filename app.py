import streamlit as st
import subprocess
import os
from datetime import datetime

# ─── Config ───────────────────────────────────────────────
st.set_page_config(page_title="PromptForge", layout="centered")

# ─── Header ───────────────────────────────────────────────
st.markdown("<h1 style='text-align: center;'>🛠️ PromptForge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sharp, clear, adaptive AI reasoning.</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── Prompt Input ─────────────────────────────────────────
user_prompt = st.text_area("💬 Ask Anything:", height=140, placeholder="e.g. Best taco recipe? Or how to optimize SQL queries?")
run = st.button("🚀 Run")

# ─── Run Pipeline ─────────────────────────────────────────
if run and user_prompt.strip():
    with st.spinner("⏳ Working on your prompt..."):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"

        output_container = st.empty()
        command = f'python3 main.py "{user_prompt}"'

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        current_step = None
        captured_output = []

        for line in process.stdout:
            line = line.strip()

            if line.startswith("✦ "):  # Step header
                current_step = line[2:]
                output_container.markdown(f"🧠 <b>{current_step}</b>", unsafe_allow_html=True)

            elif line.endswith("[Truncated]"):
                captured_output.append(f"\n\n#### {current_step}\n```\n{line.replace('[Truncated]', '').strip()}\n```")
                output_container.empty()  # Clear spinner text after step completes

            elif line != "":
                # For final response-like lines
                if current_step:
                    st.markdown(f"**{current_step}**\n\n```\n{line}\n```")
                    current_step = None  # Only show once

        process.wait()
        st.success("✅ Done!")

        # Markdown Download
        if os.path.exists(log_path):
            with open(log_path, "rb") as f:
                st.download_button("📄 Download Full Output", f, file_name=os.path.basename(log_path), mime="text/markdown")

else:
    st.info("Enter a prompt above and press **Run** to begin.")
