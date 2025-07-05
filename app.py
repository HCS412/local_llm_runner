import streamlit as st
import subprocess
import os
from datetime import datetime
from utils import sanitize_input

# ─── App Configuration ─────────────────────────────────────────────
st.set_page_config(page_title="Soulful Alignment AI", layout="wide")
st.markdown("""
    <style>
    .reportview-container .markdown-text-container {
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .step-block {
        background-color: #f9f9fa;
        border-left: 5px solid #7f7fff;
        padding: 1rem;
        margin-top: 1rem;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ─── UI Header ─────────────────────────────────────────────────────
st.title("🧠 Soulful Alignment AI")
st.caption("Co-create deeper insight through cultural critique, outsider wisdom, and human-level revision.")

# ─── Input Prompt Box ─────────────────────────────────────────────
user_prompt = st.text_area("💬 Enter your prompt for alignment:", height=180)
run_button = st.button("▶️ Run Soulful Alignment")

# ─── Alignment Trigger ─────────────────────────────────────────────
if run_button and user_prompt.strip():
    user_prompt = sanitize_input(user_prompt)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = f"logs/run_{timestamp}.md"

    with st.spinner("🧬 Running alignment process..."):
        command = f'python3 main.py "{user_prompt}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        step_name = None
        st.markdown("## 🔍 Step-by-Step Alignment")

        step_container = st.empty()
        step_markdown = ""

        for line in process.stdout:
            if "✦" in line:
                # New step begins
                step_name = line.replace("✦", "").strip()
                step_markdown += f"<div class='step-block'><h4>{step_name}</h4>\n"
            elif "[Truncated]" in line:
                step_markdown += f"<pre>{line.strip()}</pre>\n</div>\n"
            elif "..." in line or step_name:
                step_markdown += f"<code>{line.strip()}</code><br />\n"
            step_container.markdown(step_markdown, unsafe_allow_html=True)

        process.wait()

    # ─── Final Output + Download ─────────────────────────────
    st.success("✅ Alignment complete!")

    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            st.download_button(
                label="📄 Download Full Markdown Log",
                data=f,
                file_name=os.path.basename(log_path),
                mime="text/markdown"
            )
else:
    st.info("👆 Enter a prompt above and press **Run Soulful Alignment** to begin.")
