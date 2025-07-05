import streamlit as st
import subprocess
import os
from datetime import datetime

# ─── Streamlit Page Setup ──────────────────────────────────────────
st.set_page_config(page_title="PromptForge", layout="centered")
st.markdown("<h1 style='text-align: center;'>🛠️ PromptForge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sharp, clear, adaptive AI reasoning.</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── Prompt Input ──────────────────────────────────────────────────
user_prompt = st.text_area("💬 Ask Anything:", height=140, placeholder="e.g. Best taco recipe? Or how to optimize SQL queries?")
run = st.button("🚀 Run")

# ─── Run Alignment Pipeline ────────────────────────────────────────
if run and user_prompt.strip():
    with st.spinner("⏳ Running prompt through pipeline..."):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"
        command = f'python3 main.py "{user_prompt}"'

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        current_step = ""
        current_output = ""

        for line in process.stdout:
            line = line.strip()

            if line.startswith("✦ "):
                # If we had a previous step, display it first
                if current_step and current_output:
                    st.markdown(
                        f"<details><summary><b>{current_step}</b></summary><pre>{current_output.strip()}</pre></details>",
                        unsafe_allow_html=True
                    )
                    current_output = ""

                current_step = line.replace("✦ ", "").strip()

            elif "[Truncated]" in line:
                current_output += line.replace("[Truncated]", "").strip() + "\n"
                st.markdown(
                    f"<details><summary><b>{current_step} (truncated)</b></summary><pre>{current_output.strip()}...\n[Truncated]</pre></details>",
                    unsafe_allow_html=True
                )
                current_step = ""
                current_output = ""

            elif line:
                current_output += line + "\n"

        # Show last step if it exists
        if current_step and current_output:
            st.markdown(
                f"<details><summary><b>{current_step}</b></summary><pre>{current_output.strip()}</pre></details>",
                unsafe_allow_html=True
            )

        process.wait()
        st.success("✅ Response Complete!")

        if os.path.exists(log_path):
            with open(log_path, "rb") as f:
                st.download_button("📄 Download Full Output", f, file_name=os.path.basename(log_path), mime="text/markdown")

else:
    st.info("Enter a prompt above and press **Run** to begin.")
