import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# ─── Load environment ────────────────────────────────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
    build_summary_prompt
)

# ─── Print formatted section header ───────────────────────────────────
def print_section(title):
    print(f"\n\033[95m✦ {title}\033[0m")
    print("-" * (len(title) + 4) + "\n")

# ─── Truncate long LLM output for display ─────────────────────────────
def display_truncated_output(output, limit=1000):
    if len(output) > limit:
        print(output[:limit] + "\n... [Truncated]")
    else:
        print(output)

# ─── Save run to Markdown log ─────────────────────────────────────────
def save_markdown_log(prompt, steps):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"logs/run_{timestamp}.md"
    with open(path, "w") as f:
        f.write(f"# 🌱 Alignment Run - {timestamp}\n\n")
        f.write(f"## Prompt\n{prompt}\n\n")
        for step in steps:
            f.write(f"## {step['title']}\n{step['output']}\n\n")
    print(f"\n✅ Output saved to {path}")

# ─── Main orchestration pipeline ──────────────────────────────────────
def run_pipeline(user_prompt):
    steps = []
    principles = load_principles()

    def run_step(title, builder_fn, *args):
        print_section(title)
        prompt = builder_fn(*args)
        output = call_local_llm(prompt, max_tokens=500)
        display_truncated_output(output)
        steps.append({"title": title, "prompt": prompt, "output": output})
        return output

    # ─── Prompt-type classification ─────────────────────────────
    lowered = user_prompt.lower()
    if any(word in lowered for word in ["build", "design", "code", "implement", "api", "database", "tech", "python", "algorithm"]):
        prompt_type = "technical"
    elif any(word in lowered for word in ["justice", "race", "gender", "equity", "identity", "culture", "marginalized"]):
        prompt_type = "social"
    elif any(word in lowered for word in ["startup", "founder", "investor", "fund", "venture", "capital", "business"]):
        prompt_type = "venture"
    else:
        prompt_type = "default"

    print(f"\033[94m📌 Detected prompt type:\033[0m {prompt_type}\n")

    # ─── Step 1: Always run initial prompt ─────────────────────
    initial = run_step("🧠 Step 1: Initial Response", build_initial_prompt, user_prompt)

    # ─── Steps 2–3: Skipped for 'technical' prompts ────────────
    if prompt_type != "technical":
        critique = run_step("🔍 Step 2: Critique v1 (Outsider Principles)", build_critique_prompt, initial, principles)
        deeper_critique = run_step("🕳️ Step 3: Expand Critique (What's Missing?)", build_deep_dive_prompt, critique)
    else:
        critique = ""
        deeper_critique = ""

    # ─── Step 4: Perspective shift ─────────────────────────────
    persona_echo = run_step("🎭 Step 4: Persona Echo (Perspective Shift)", build_persona_echo_prompt, initial)

    # ─── Step 5: Combine & revise ─────────────────────────────
    revised = run_step("🔧 Step 5: Revision (Incorporate All)", build_revise_prompt, initial, critique, deeper_critique, persona_echo)

    # ─── Steps 6–8: Only for deep or social prompts ───────────
    if prompt_type not in ["technical"]:
        second_critique = run_step("🔎 Step 6: Second Critique (Refined Response)", build_second_critique_prompt, revised, principles)
        tensions = run_step("🪞 Step 7: Reflect on Tensions", build_tension_prompt, revised)
        soul = run_step("💀 Step 8: Meta-Soul Check", build_meta_soul_prompt, user_prompt, revised)

    # ─── Step 9: Always summarize ─────────────────────────────
    summary = run_step("📈 Step 9: Growth + Summary", build_summary_prompt, initial, revised)

    # ─── Save log ──────────────────────────────────────────────
    save_markdown_log(user_prompt, steps)

# ─── Entry point ─────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    run_pipeline(user_prompt)
