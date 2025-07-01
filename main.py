# main.py

import sys
import os
from datetime import datetime

from llm_client import call_local_llm
from prompt_builder import (
    load_principles,
    build_initial_prompt,
    build_critique_prompt,
    build_revise_prompt,
    build_reflection_prompt
)

def print_section(title):
    print(f"\n\033[95m✦ {title}\033[0m")
    print("-" * (len(title) + 4))

def save_markdown_log(prompt, initial, critique, revised, reflection):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"logs/run_{timestamp}.md"
    with open(path, "w") as f:
        f.write(f"# 🌱 Alignment Run - {timestamp}\n\n")
        f.write(f"## 🧠 Prompt\n{prompt}\n\n")
        f.write(f"## 📝 Initial Response\n{initial}\n\n")
        f.write(f"## 🔍 Critique\n{critique}\n\n")
        f.write(f"## 🔧 Revised\n{revised}\n\n")
        f.write(f"## 🪞 Reflection\n{reflection}\n")
    print(f"\n✅ Output saved to {path}")

def run_pipeline(user_prompt):
    principles = load_principles()

    print_section("🧠 Original Prompt")
    print(user_prompt)

    print_section("✍️ Step 1: Generate Initial Response")
    initial = call_local_llm(build_initial_prompt(user_prompt))
    print(initial)

    print_section("🧾 Step 2: Critique with Outsider Principles")
    critique = call_local_llm(build_critique_prompt(initial, principles))
    print(critique)

    print_section("🛠️ Step 3: Revise Based on Critique")
    revised = call_local_llm(build_revise_prompt(initial, critique))
    print(revised)

    print_section("🪞 Step 4: Reflect on the Transformation")
    reflection = call_local_llm(build_reflection_prompt(initial, revised))
    print(reflection)

    save_markdown_log(user_prompt, initial, critique, revised, reflection)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    run_pipeline(user_prompt)
