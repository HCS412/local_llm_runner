import streamlit as st
import subprocess
import os
from datetime import datetime

# ─── Set page configuration ─────────────────────────────
st.set_page_config(page_title="Soulful Alignment AI", layout="centered")

# ─── Title & Description ────────────────────────────────
st.markdown("# 🧠 Soulful Alignment AI")
st.markdown("Reflect, critique, and revise your ideas with cultural insight and philosophical depth.")

# ─── Prompt Input ───────────────────────────────────────
user_prompt = st.text_area("💬 Enter your prompt:", height=150)
run_button = st.button("▶️ Run Alignment")

# ─── Run Pipeline ───────────────────────────────────────
if run_button and user_prompt.strip():
    with st.spinner("🧠 Thinking through your prompt..."):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"

        command = f'python3 main.py "{user_prompt}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        output_lines = []
        step_name = None

        st.markdown("## 🔍 Step-by-Step Reasoning\n")

        for line in process.stdout:
            output_lines.append(line)
            if "✦" in line:
                step_name = line.strip().replace("✦ ", "")
                st.markdown(f"### 🪜 {step_name}")
            elif step_name and "[Truncated]" in line:
                st.markdown(f"```text\n{line.strip()}```")
            elif step_name and "..." in line:
                st.markdown(f"`{line.strip()}`")

        process.wait()

        st.success("✅ Alignment complete! See logs folder for full markdown.")
        if os.path.exists(log_path):
            with open(log_path, "rb") as f:
                st.download_button("📄 Download Markdown Output", f, file_name=os.path.basename(log_path), mime="text/markdown")
else:
    st.info("Enter a prompt above and press **Run Alignment** to begin.")
