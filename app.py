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
    with st.spinner("⏳ Running reasoning pipeline..."):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"
        command = f'python3 main.py "{user_prompt}"'

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        current_step = None
        current_block = ""
        steps = []

        # Parse output step-by-step
        for line in process.stdout:
            line = line.strip()

            if line.startswith("✦ "):
                # Save previous step before starting a new one
                if current_step and current_block:
                    steps.append((current_step, current_block.strip()))
                    current_block = ""

                current_step = line.replace("✦ ", "").strip()

            elif line:
                current_block += line + "\n"

        # Capture final block
        if current_step and current_block:
            steps.append((current_step, current_block.strip()))

        process.wait()

    # ─── Display Output ───────────────────────────────────────
    st.success("✅ Response Complete!")
    for step_title, step_content in steps:
        st.markdown(
            f"<details><summary><b>{step_title}</b></summary><pre>{step_content}</pre></details>",
            unsafe_allow_html=True
        )

    # ─── Suggest Follow-Up ────────────────────────────────────
    if steps:
        last_output = steps[-1][1].strip()
        if not last_output.endswith("?"):
            st.markdown("💡 *Need more clarity or depth? Try a follow-up prompt!*")

    # ─── Markdown Download ───────────────────────────────────
    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            st.download_button("📄 Download Full Markdown Output", f, file_name=os.path.basename(log_path), mime="text/markdown")

else:
    st.info("Enter a prompt above and press **Run** to begin.")
