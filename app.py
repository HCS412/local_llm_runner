
import streamlit as st
import subprocess
import os
import time
import re
from datetime import datetime

# ─── Config ───────────────────────────────────────────────
st.set_page_config(page_title="PromptForge", layout="centered")

# ─── Header ───────────────────────────────────────────────
st.markdown("<h1 style='text-align: center;'>🛠️ PromptForge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sharp, clear, adaptive AI reasoning.</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── Session State for Follow-Up Autofill ────────────────
if "autofill_prompt" not in st.session_state:
    st.session_state.autofill_prompt = ""

# ─── Prompt Input ─────────────────────────────────────────
user_prompt = st.text_area("💬 Ask Anything:", height=140, placeholder="e.g. Best taco recipe? Or how to optimize SQL queries?")
run = st.button("🚀 Run")

# ─── Run Pipeline ─────────────────────────────────────────
if run and user_prompt.strip():
    with st.spinner("⏳ Working on your prompt..."):
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"

        command = f'python3 main.py "{user_prompt}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        raw_output_lines = []
        cleaned_output_lines = []
        followups = []

        for line in process.stdout:
            raw_output_lines.append(line)
            clean_line = line.strip()

            if clean_line.startswith("/") or "site-packages" in clean_line or "warnings.warn" in clean_line:
                continue

            if "🤔 Follow-Up:" in clean_line or "Follow-Up:" in clean_line:
                followup_matches = re.findall(r"[🤔📌🌮🧠🔁📎💡]?\s*(.+?)(?:\?|$)", clean_line.split("Follow-Up:")[-1])
                followups.extend([f.strip().strip("?") for f in followup_matches if f.strip()])
                continue

            if "Detected prompt type" in clean_line or "✦" in clean_line:
                cleaned_output_lines.append(f"📌 <b>{clean_line.replace('✦', '').strip()}</b>")
            elif clean_line:
                cleaned_output_lines.append(clean_line)

        process.wait()
        elapsed = round(time.time() - start_time, 1)

        st.success(f"✅ Response Complete in {elapsed} seconds")

        st.markdown("<details><summary>📄 <b>View Clean Output</b></summary>", unsafe_allow_html=True)
        for line in cleaned_output_lines:
            st.markdown(line, unsafe_allow_html=True)
        st.markdown("</details>", unsafe_allow_html=True)

        if followups:
            st.markdown("### 🔁 Suggested Follow-Ups:")
            cols = st.columns(len(followups))
            for i, suggestion in enumerate(followups):
                with cols[i]:
                    if st.button(suggestion):
                        st.session_state.autofill_prompt = suggestion
                        st.experimental_rerun()

        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                raw_output = f.read()
            with st.expander("🪵 Raw Output (Debug)", expanded=False):
                st.code(raw_output)
            with open(log_path, "rb") as f:
                st.download_button("📥 Download Full Output", f, file_name=os.path.basename(log_path), mime="text/markdown")

else:
    if st.session_state.autofill_prompt:
        user_prompt = st.session_state.autofill_prompt
        st.session_state.autofill_prompt = ""
        st.experimental_rerun()
    else:
        st.info("Enter a prompt above and press **Run** to begin.")
