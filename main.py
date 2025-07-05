import sys
import os
from datetime import datetime
from dotenv import load_dotenv

from llm_client import call_local_llm
from prompt_builder import (
    load_principles,
    build_initial_prompt,
    build_critique_prompt,
    build_deep_dive_prompt,
    build_persona_echo_prompt,
    build_revise_prompt,
    build_second_critique_prompt,
    build_tension_prompt,
    build_meta_soul_prompt,
    build_summary_prompt,
)
from utils import (
    detect_prompt_type,
    format_step_header,
    truncate_output,
    sanitize_input,
    is_simple_question,
    suggest_followup  # NEW for follow-up prompts
)

# ─── Load .env ─────────────────────────────────────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# ─── Save run to Markdown ──────────────────────────────────────────
def save_markdown_log(prompt, steps):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"logs/run_{timestamp}.md"
    with open(path, "w") as f:
        f.write(f"# 🛠️ PromptForge Run - {timestamp}\n\n")
        f.write(f"## Prompt\n{prompt}\n\n")
        for step in steps:
            f.write(f"## {step['title']}\n{step['output']}\n\n")
    print(f"\n✅ Output saved to {path}")

# ─── Orchestration Pipeline ────────────────────────────────────────
def run_pipeline(user_prompt):
    user_prompt = sanitize_input(user_prompt)
    prompt_type = detect_prompt_type(user_prompt)
    print(f"\033[94m📌 Detected prompt type:\033[0m {prompt_type}\n")

    steps = []

    def run_step(title, builder_fn, *args, max_tokens=200):
        print(format_step_header(title))
        prompt = builder_fn(*args)
        output = call_local_llm(prompt, max_tokens=max_tokens)
        print(truncate_output(output))
        steps.append({"title": title, "prompt": prompt, "output": output})
        return output

    # ─── Fast path for simple prompts ───────────────────────────────
    if is_simple_question(user_prompt):
        response = run_step("⚡ Simple Response", build_initial_prompt, user_prompt, prompt_type, max_tokens=300)

        followup = suggest_followup(user_prompt)
        if followup:
            print(f"\n🤔 Follow-Up: {followup}")
            steps.append({"title": "💬 Follow-Up Suggestion", "prompt": "", "output": followup})

        save_markdown_log(user_prompt, steps)
        return

    # ─── Full pipeline ───────────────────────────────────────────────
    principles = load_principles()

    initial = run_step("🧠 Step 1: Initial Response", build_initial_prompt, user_prompt, prompt_type)

    if prompt_type != "technical":
        critique = run_step("🔍 Step 2: Critique v1 (Outsider Principles)", build_critique_prompt, initial, principles)
        deeper_critique = run_step("🕳️ Step 3: Expand Critique (What's Missing?)", build_deep_dive_prompt, critique)
    else:
        critique = ""
        deeper_critique = ""

    persona_echo = run_step("🎭 Step 4: Persona Echo (Perspective Shift)", build_persona_echo_prompt, initial, prompt_type)

    revised = run_step("🔧 Step 5: Revision (Incorporate All)", build_revise_prompt, initial, critique, deeper_critique, persona_echo)

    if prompt_type not in ["technical"]:
        run_step("🔎 Step 6: Second Critique (Refined Response)", build_second_critique_prompt, revised, principles)
        run_step("🪞 Step 7: Reflect on Tensions", build_tension_prompt, revised)
        run_step("💀 Step 8: Meta-Soul Check", build_meta_soul_prompt, user_prompt, revised)

    run_step("📈 Step 9: Growth + Summary", build_summary_prompt, initial, revised, max_tokens=500)

    save_markdown_log(user_prompt, steps)

# ─── CLI Entrypoint ────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    run_pipeline(user_prompt)
