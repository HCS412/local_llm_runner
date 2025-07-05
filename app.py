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
user_prompt = st.text_area(
    "💬 Ask Anything:", 
    height=140, 
    placeholder="e.g. Best taco recipe? Or how to optimize SQL queries?"
)
run = st.button("🚀 Run")

# ─── Run Pipeline ─────────────────────────────────────────
if run and user_prompt.strip():
    with st.spinner("⏳ Working on your prompt..."):
        start_time = datetime.now()
        timestamp = start_time.strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"

        output_container = st.empty()
        full_output = ""
        current_step = ""

        command = f'python3 main.py "{user_prompt}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            line = line.strip()

            # Ignore noisy system warnings or paths
            if line.startswith("/") or "site-packages" in line or "warnings.warn" in line:
                continue

            # Prompt type or step title
            if line.startswith("✦ "):
                current_step = line.replace("✦ ", "").strip()
                output_container.markdown(f"🧠 <b>{current_step}</b>", unsafe_allow_html=True)

            # Append response content
            elif line:
                full_output += line + "\n"

        process.wait()
        end_time = datetime.now()
        elapsed = round((end_time - start_time).total_seconds(), 2)

        # Final output
        output_container.markdown("✅ <b>Response Complete!</b>", unsafe_allow_html=True)
        st.success(f"✅ Response Complete in {elapsed} seconds")

        # Display full result in collapsible section
        st.markdown(
            f"<details><summary><b>📄 View Full Output</b></summary><pre style='white-space: pre-wrap;'>{full_output}</pre></details>",
            unsafe_allow_html=True
        )

        # Clipboard copy button
        escaped_output = full_output.replace("`", "'").replace("\\", "\\\\")
        st.markdown(
            f"""
            <button onclick="navigator.clipboard.writeText(`{escaped_output}`)"
                    style="margin-top: 10px; padding: 6px 12px; border-radius: 5px; background-color: #444; color: white; border: none; cursor: pointer;">
                📋 Copy Full Output
            </button>
            """,
            unsafe_allow_html=True
        )

        # Save to file and offer download
        os.makedirs("logs", exist_ok=True)
        with open(log_path, "w") as f:
            f.write(full_output)

        with open(log_path, "rb") as f:
            st.download_button("📥 Download Output", f, file_name=os.path.basename(log_path), mime="text/markdown")

else:
    st.info("Enter a prompt above and press **Run** to begin.")
