# pipelines/venture_pipeline.py

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
    format_step_header,
    truncate_output,
    sanitize_input,
    is_simple_question,
    suggest_followup,
)
from datetime import datetime
import os


def run_pipeline(user_prompt: str, prompt_type: str = "venture"):
    user_prompt = sanitize_input(user_prompt)
    print(f"\033[94m📌 [VenturePipeline] Prompt type:\033[0m {prompt_type}\n")

    steps = []

    def run_step(title, builder_fn, *args, max_tokens=200):
        print(format_step_header(title))
        prompt = builder_fn(*args)
        output = call_local_llm(prompt, max_tokens=max_tokens)
        print(truncate_output(output))
        steps.append({"title": title, "prompt": prompt, "output": output})
        return output

    if is_simple_question(user_prompt):
        response = run_step("⚡ Venture Insight", build_initial_prompt, user_prompt, prompt_type, max_tokens=300)

        followup = suggest_followup(user_prompt)
        if followup:
            print(f"\n🤔 Follow-Up: {followup}")
            steps.append({"title": "💬 Follow-Up Suggestion", "prompt": "", "output": followup})

        save_markdown_log(user_prompt, steps)
        return

    principles = load_principles()

    initial = run_step("📊 Step 1: Startup Response", build_initial_prompt, user_prompt, prompt_type)
    critique = run_step("🔍 Step 2: Outsider Critique", build_critique_prompt, initial, principles)
    deep = run_step("🕳️ Step 3: What's Missing?", build_deep_dive_prompt, critique)
    echo = run_step("🎭 Step 4: Shift Perspective", build_persona_echo_prompt, initial, prompt_type)
    revised = run_step("💼 Step 5: Pitch Rework", build_revise_prompt, initial, critique, deep, echo)
    run_step("🧠 Step 6: Sharpen Again", build_second_critique_prompt, revised, principles)
    run_step("⚖️ Step 7: Narrative Tension", build_tension_prompt, revised)
    run_step("💀 Step 8: Meta-Soul Check", build_meta_soul_prompt, user_prompt, revised)
    run_step("🚀 Step 9: Summary + GTM", build_summary_prompt, initial, revised, max_tokens=500)

    save_markdown_log(user_prompt, steps)


def save_markdown_log(prompt, steps):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"logs/run_{timestamp}.md"
    with open(path, "w") as f:
        f.write(f"# 🚀 Venture Pipeline - {timestamp}\n\n")
        f.write(f"## Prompt\n{prompt}\n\n")
        for step in steps:
            f.write(f"## {step['title']}\n{step['output']}\n\n")
    print(f"\n✅ Output saved to {path}")
