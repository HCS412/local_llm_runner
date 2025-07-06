# pipelines/simple_pipeline.py

from llm_client import call_local_llm
from prompt_builder import build_initial_prompt
from utils import (
    format_step_header,
    truncate_output,
    sanitize_input,
    suggest_followup,
)
from datetime import datetime
import os


def run_pipeline(user_prompt: str, prompt_type: str = "default"):
    user_prompt = sanitize_input(user_prompt)
    print(f"\033[94m📌 [SimplePipeline] Prompt type:\033[0m {prompt_type}\n")

    steps = []

    def run_step(title, prompt_fn, *args, max_tokens=300):
        print(format_step_header(title))
        prompt = prompt_fn(*args)
        output = call_local_llm(prompt, max_tokens=max_tokens)
        print(truncate_output(output))
        steps.append({"title": title, "prompt": prompt, "output": output})
        return output

    output = run_step("⚡ Quick Response", build_initial_prompt, user_prompt, prompt_type)

    followup = suggest_followup(user_prompt)
    if followup:
        print(f"\n🤔 Follow-Up: {followup}")
        steps.append({"title": "💬 Follow-Up Suggestion", "prompt": "", "output": followup})

    save_markdown_log(user_prompt, steps)


def save_markdown_log(prompt, steps):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"logs/run_{timestamp}.md"
    with open(path, "w") as f:
        f.write(f"# ⚡ Simple Pipeline - {timestamp}\n\n")
        f.write(f"## Prompt\n{prompt}\n\n")
        for step in steps:
            f.write(f"## {step['title']}\n{step['output']}\n\n")
    print(f"\n✅ Output saved to {path}")
