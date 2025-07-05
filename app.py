import streamlit as st
import subprocess
import os
from datetime import datetime

# ─── Branding ──────────────────────────────────────────────
st.set_page_config(page_title="PromptForge", layout="centered")

st.markdown("<h1 style='text-align: center;'>🛠️ PromptForge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Refine and evolve your ideas with clarity and perspective.</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── Prompt Input ──────────────────────────────────────────
user_prompt = st.text_area("💬 Your Prompt:", height=150, placeholder="e.g. How do I optimize a SQL query for performance on large datasets?")
run = st.button("⚡ Forge Response")

# ─── Run Alignment Pipeline ────────────────────────────────
if run and user_prompt.strip():
    with st.spinner("🧠 Analyzing prompt type..."):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"

        st.markdown("### 🧩 Running Pipeline\n")

        command = f'python3 main.py "{user_prompt}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        output_lines = []
        step_container = st.empty()
        current_step = ""

        for line in process.stdout:
            output_lines.append(line)

            if "✦" in line:
                current_step = line.strip().replace("✦ ", "")
                step_container.markdown(f"⏳ <b>{current_step}</b>", unsafe_allow_html=True)
            elif "[Truncated]" in line or "... [" in line:
                step_container.markdown("")  # Clear after done
                st.markdown(f"<details><summary>{current_step}</summary><pre>{line.strip()}</pre></details>", unsafe_allow_html=True)

        process.wait()
        step_container.markdown("✅ Done!")

        if os.path.exists(log_path):
            with open(log_path, "rb") as f:
                st.download_button("📄 Download Full Markdown Output", f, file_name=os.path.basename(log_path), mime="text/markdown")

else:
    st.info("Enter a prompt above and press **⚡ Forge Response** to begin.")
