import streamlit as st
import subprocess
import os
import sys
import time
import re
import json
from datetime import datetime
from uuid import uuid4

# ─── Add local directory to Python path ───────────────────
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ─── Local Imports ────────────────────────────────────────
from run_llm import run_llm
from utils.prompt_classifier import classify_prompt
from utils.prompt_router import route_prompt

# ─── Streamlit Page Config ────────────────────────────────
st.set_page_config(page_title="PromptForge", layout="centered")

st.markdown("<h1 style='text-align: center;'>🛠️ PromptForge</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sharp, clear, adaptive AI reasoning.</p>", unsafe_allow_html=True)
st.markdown("---")

# ─── Session State ────────────────────────────────────────
if "autofill_prompt" not in st.session_state:
    st.session_state.autofill_prompt = ""

# ─── Prompt Input ─────────────────────────────────────────
user_prompt = st.text_area("💬 Ask Anything:", height=140, placeholder="e.g. Best taco recipe? Or how to optimize SQL queries?")
run = st.button("🚀 Run")

# ─── Run Logic ────────────────────────────────────────────
if run and user_prompt.strip():
    with st.spinner("⏳ Working on your prompt..."):
        start_time = time.time()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = f"logs/run_{timestamp}.md"

        # 🧠 Step 1: Classify prompt type using LLM
        with st.expander("🧠 Prompt Type (Auto-Classified)", expanded=False):
            try:
                prompt_type = classify_prompt(user_prompt, run_llm)
                st.markdown(f"Detected: **{prompt_type}**")
            except Exception as e:
                st.error(f"Prompt classification failed: {e}")
                prompt_type = "default"

        # 🔀 Step 2: Decide routing
        mode = route_prompt(user_prompt, prompt_type)

        if mode == "simple":
            response = run_llm(user_prompt)
            elapsed = round(time.time() - start_time, 1)
            st.success(f"✅ Simple LLM Response in {elapsed} seconds")
            st.markdown(f"### 🧠 Answer:\n\n{response}")
        else:
            command = f'python3 main.py "{user_prompt}"'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            raw_output_lines = []
            cleaned_output_lines = []
            followups = []
            step_blocks = []
            current_step = []
            current_title = None

            for line in process.stdout:
                raw_output_lines.append(line)
                clean_line = line.strip()

                if clean_line.startswith("/") or "site-packages" in clean_line or "warnings.warn" in clean_line:
                    continue

                if "🤔 Follow-Up:" in clean_line or "Follow-Up:" in clean_line:
                    followup_matches = re.findall(r"[🤔📌🌮🧠🔁📎💡]?\s*(.+?)(?:\?|$)", clean_line.split("Follow-Up:")[-1])
                    followups.extend([f.strip().strip("?") for f in followup_matches if f.strip()])
                    continue

                if clean_line.startswith("##"):
                    if current_title and current_step:
                        step_blocks.append({"title": current_title, "output": "\n".join(current_step)})
                    current_title = clean_line.replace("##", "").strip()
                    current_step = []
                elif clean_line:
                    current_step.append(clean_line)

            if current_title and current_step:
                step_blocks.append({"title": current_title, "output": "\n".join(current_step)})

            process.wait()
            elapsed = round(time.time() - start_time, 1)
            st.success(f"✅ Response Complete in {elapsed} seconds")

            st.markdown("### 🧠 Step-by-Step Output")
            for step in step_blocks:
                with st.expander(f"🔎 {step['title']}", expanded=True):
                    st.markdown(f"<div style='background-color:#111827;padding:10px;border-radius:10px;'>", unsafe_allow_html=True)
                    st.markdown(step["output"])
                    st.markdown("</div>", unsafe_allow_html=True)

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
