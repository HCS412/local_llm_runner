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
    build_summary_prompt
)

# ─── Load environment variables ───────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# ─── Colored section header ───────────────────────────
def print_section(title):
    print(f"\n\033[95m✦ {title}\033[0m")
    print("-" * (len(title) + 4) + "\n")

# ─── Save full markdown log to /logs ─────────────────
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

# ─── Truncate wall of text in terminal ───────────────
def display_truncated_output(output, limit=1000):
    if len(output) > limit:
        print(output[:limit].strip() + "\n...\n[Truncated]")
    else:
        print(output.strip())

# ─── Choose response mode dynamically ────────────────
def detect_mode(prompt):
    if any(x in prompt.lower() for x in ["equity", "justice", "marginalized", "systemic", "race", "gender"]):
        return "soulful"
    elif any(x in prompt.lower() for x in ["venture", "startup", "investing", "product", "distribution", "growth", "capital"]):
        return "strategic"
    else:
        return "neutral"

# ─── Main pipeline ───────────────────────────────────
def run_pipeline(user_prompt):
    steps = []
    mode = detect_mode(user_prompt)
    principles = load_principles()

    def run_step(title, builder_fn, *args):
        print_section(title)
        print("\033[90m[Thinking...]\033[0m")
        prompt = builder_fn(*args)
        output = call_local_llm(prompt, max_tokens=200, mode=mode)
        display_truncated_output(output)
        steps.append({"title": title, "prompt": prompt, "output": output})
        return output

    initial = run_step("🧠 Step 1: Initial Response", build_initial_prompt, user_prompt)
    critique = run_step("🔍 Step 2: Critique v1 (Outsider Principles)", build_critique_prompt, initial, principles)
    deeper_critique = run_step("🕳️ Step 3: Expand Critique (What's Missing?)", build_deep_dive_prompt, critique)
    persona_echo = run_step("🎭 Step 4: Persona Echo (Perspective Shift)", build_persona_echo_prompt, initial)
    revised = run_step("🔧 Step 5: Revision (Incorporate All)", build_revise_prompt, initial, critique, deeper_critique, persona_echo)
    second_critique = run_step("🔎 Step 6: Second Critique (Refined Response)", build_second_critique_prompt, revised, principles)
    tensions = run_step("🪞 Step 7: Reflect on Tensions", build_tension_prompt, revised)
    soul = run_step("💀 Step 8: Meta-Soul Check", build_meta_soul_prompt, user_prompt, revised)
    summary = run_step("📈 Step 9: Growth + Summary", build_summary_prompt, initial, revised)

    save_markdown_log(user_prompt, steps)

# ─── Entry point ─────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)
    user_prompt = " ".join(sys.argv[1:])
    run_pipeline(user_prompt)
