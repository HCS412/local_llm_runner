import sys
import os
from dotenv import load_dotenv
from utils.prompt_classifier import classify_prompt
from pipelines.router import route_and_run_pipeline
from utils import sanitize_input

# ─── Load .env ─────────────────────────────────────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# ─── Orchestration Pipeline ────────────────────────────────────────
def run_pipeline(user_prompt):
    user_prompt = sanitize_input(user_prompt)
    prompt_type = classify_prompt(user_prompt)
    print(f"\033[94m📌 Detected prompt type:\033[0m {prompt_type}\n")

    # Modular pipeline routing
    route_and_run_pipeline(prompt_type, user_prompt)

# ─── CLI Entrypoint ────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    run_pipeline(user_prompt)
