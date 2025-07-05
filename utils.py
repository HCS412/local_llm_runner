# utils.py

import re
import textwrap

# ──────────────────────────────────────────────────────────────────────
# Prompt Classification
# ──────────────────────────────────────────────────────────────────────
def detect_prompt_type(prompt: str) -> str:
    prompt = prompt.lower()
    tech_keywords = ["build", "design", "code", "implement", "api", "database", "python", "algorithm"]
    social_keywords = ["justice", "race", "gender", "equity", "identity", "culture", "marginalized"]
    venture_keywords = ["startup", "founder", "investor", "fund", "venture", "capital", "business"]

    if any(k in prompt for k in tech_keywords):
        return "technical"
    elif any(k in prompt for k in social_keywords):
        return "social"
    elif any(k in prompt for k in venture_keywords):
        return "venture"
    else:
        return "default"

# ──────────────────────────────────────────────────────────────────────
# Output Truncation
# ──────────────────────────────────────────────────────────────────────
def truncate_output(output: str, limit: int = 800) -> str:
    return output[:limit] + "\n... [Truncated]" if len(output) > limit else output

# ──────────────────────────────────────────────────────────────────────
# Format CLI Step Headers
# ──────────────────────────────────────────────────────────────────────
def format_step_header(title: str) -> str:
    return f"\n\033[95m✦ {title}\033[0m\n" + "-" * (len(title) + 4) + "\n"

# ──────────────────────────────────────────────────────────────────────
# Shell/Markdown Safe Input
# ──────────────────────────────────────────────────────────────────────
def sanitize_input(prompt: str) -> str:
    return re.sub(r'[^\x00-\x7F]+', ' ', prompt).strip()

# ──────────────────────────────────────────────────────────────────────
# Soft Wrap for Streamlit
# ──────────────────────────────────────────────────────────────────────
def soft_wrap(text: str, width: int = 100) -> str:
    return "\n".join(textwrap.wrap(text, width))
