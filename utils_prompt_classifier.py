import re

# ─── LLM-Driven Prompt Classification ───────────────────────────────
def classify_prompt(prompt: str, run_llm) -> str:
    """Use an LLM to classify the prompt type. Fallback to rules if needed."""
    system_prompt = (
        "You are a precise classification engine. Categorize the following prompt into "
        "one of these types:\n"
        "- simple_response: asks for a straightforward or short answer (e.g., 'how do I boil an egg?')\n"
        "- creative_generation: requests ideas, names, recipes, stories, etc.\n"
        "- analytical_question: requires structured reasoning or multi-step logic\n"
        "- personal_request: involves subjective, emotional, or contextual user info\n"
        "- technical_prompt: related to code, APIs, software, databases, etc.\n\n"
        "Respond ONLY with one of these exact labels."
    )

    try:
        response = run_llm(system_prompt, prompt).strip().lower()
        if response in [
            "simple_response", "creative_generation",
            "analytical_question", "personal_request", "technical_prompt"
        ]:
            return response
    except Exception:
        pass  # fallback if LLM fails

    # ─── Fallback Classification Logic ──────────────────────────────
    lowered = prompt.lower()
    word_count = len(lowered.split())

    if any(word in lowered for word in [
        "build", "code", "api", "function", "model", "python", "sql", "query", "script"
    ]):
        return "technical_prompt"
    elif any(word in lowered for word in [
        "how do i", "what is", "best way to", "steps to", "explain", "overview", "list of", "simple guide"
    ]) and word_count < 25:
        return "simple_response"
    elif any(word in lowered for word in [
        "give me ideas", "suggest", "generate", "make up", "create", "write a story", "recipe"
    ]):
        return "creative_generation"
    elif any(word in lowered for word in [
        "thoughts on", "help me understand", "pros and cons", "should i", "what are the implications"
    ]):
        return "analytical_question"
    elif any(word in lowered for word in [
        "i feel", "my experience", "my girlfriend", "as a", "my son", "my daughter", "my job", "my startup"
    ]):
        return "personal_request"
    else:
        return "simple_response"
