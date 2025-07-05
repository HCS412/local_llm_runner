import re

# ─── Clean input ─────────────────────────────────────────────────────
def sanitize_input(prompt: str) -> str:
    return prompt.strip().replace("\n", " ")

# ─── Format CLI step headers ─────────────────────────────────────────
def format_step_header(title: str) -> str:
    return f"\n\033[95m✦ {title}\033[0m\n{'-' * (len(title) + 4)}\n"

# ─── Truncate long output for display ───────────────────────────────
def truncate_output(text: str, limit: int = 1000) -> str:
    if not text:
        return "[No Output]"
    clean = text.strip().replace("\r", "").replace("undefined", "")
    return clean[:limit] + "\n... [Truncated]" if len(clean) > limit else clean

# ─── Prompt type classification ─────────────────────────────────────
def detect_prompt_type(prompt: str) -> str:
    lowered = prompt.lower()
    if any(word in lowered for word in ["build", "design", "code", "implement", "api", "database", "python", "query", "algorithm"]):
        return "technical"
    elif any(word in lowered for word in ["justice", "race", "gender", "equity", "identity", "culture", "marginalized", "bias"]):
        return "social"
    elif any(word in lowered for word in ["startup", "founder", "investor", "fund", "venture", "capital", "pitch", "lp", "deal"]):
        return "venture"
    else:
        return "default"

# ─── Detect trivial/simple prompt ────────────────────────────────────
def is_simple_question(prompt: str) -> bool:
    simple_keywords = [
        "recipe", "how do i", "what is", "tips for", "best way to", "how to", "suggestions for",
        "give me a list", "recommend", "simple guide", "quick answer", "explain", "overview of",
        "summary of", "steps to", "list of"
    ]
    lowered = prompt.lower()
    short_enough = len(lowered.split()) < 25
    return any(kw in lowered for kw in simple_keywords) and short_enough

# ─── Dynamic follow-up suggestions for simple prompts ────────────────
def suggest_followup(prompt: str) -> str:
    prompt = prompt.lower()

    if "taco" in prompt:
        return "🌮 Want it spicy or mild? Would you like a vegetarian version too?"
    if "recipe" in prompt:
        return "👩‍🍳 Any dietary restrictions or cuisine types you prefer?"
    if "travel" in prompt:
        return "✈️ Would you like off-the-beaten-path suggestions or popular spots?"
    if "book" in prompt:
        return "📚 Would you prefer fiction or nonfiction? Light or intense?"
    if "startup" in prompt:
        return "🚀 Do you want funding strategy advice or product-market fit tips?"

    return "💬 Want to go deeper or see alternatives?"
