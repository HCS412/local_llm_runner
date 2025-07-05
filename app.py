import streamlit as st
import subprocess
import os
import time
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
    start_time = time.time()
    with st.spinner("⏳ Analyzing your prompt and generating response..."):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"

        command = f'python3 main.py "{user_prompt}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        steps_output = []
        final_output_lines = []
        current_step = ""

        for line in process.stdout:
            line = line.strip()

            # Skip noisy logs
            if "/venv/" in line or "warnings.warn(" in line or "site-packages" in line:
                continue

            # Detect pipeline step
            if line.startswith("✦ "):
                current_step = line.replace("✦ ", "").strip()
                steps_output.append(f"### 🧩 {current_step}\n")
            elif line:
                # Group outputs
                if current_step:
                    steps_output.append(f"```\n{line}\n```\n")
                final_output_lines.append(line)

        process.wait()
        full_output = "\n".join(final_output_lines)
        steps_md = "\n".join(steps_output)
        elapsed = round(time.time() - start_time, 2)

        # ─── Tabs for Steps & Final Output ─────────────────────
        tabs = st.tabs(["🪜 Pipeline Steps", "🧠 Final Output"])
        with tabs[0]:
            st.markdown(steps_md, unsafe_allow_html=True)

        with tabs[1]:
            st.code(full_output, language="markdown")
            st.download_button("📄 Download Markdown", full_output, file_name=os.path.basename(log_path), mime="text/markdown")

            # Copy to clipboard
            st.markdown(f"""
                <button onclick="navigator.clipboard.writeText(`{full_output.replace("`", "\\`")}`)"
                        style="margin-top: 10px; padding: 6px 12px; border-radius: 5px; background-color: #444; color: white; border: none; cursor: pointer;">
                    📋 Copy to Clipboard
                </button>
            """, unsafe_allow_html=True)

            st.success(f"✅ Response Complete in {elapsed} seconds")

# ─── Idle Message ──────────────────────────────────────────
else:
    st.info("Enter a prompt above and press **Run** to begin.")

# ─── Footer / CTA ──────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 0.9em;'>🔗 <i>Coming soon: Share PromptForge with your friends. Built with love + local LLMs.</i></p>",
    unsafe_allow_html=True
)
