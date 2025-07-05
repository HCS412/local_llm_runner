# utils/prompt_router.py

def route_prompt(prompt: str, prompt_type: str) -> str:
    """
    Determines whether to run a simple LLM call or full critique pipeline.
    
    Args:
        prompt (str): User's original prompt
        prompt_type (str): Classified type from the LLM

    Returns:
        str: "simple" or "full_pipeline"
    """

    # Normalize prompt
    prompt = prompt.lower().strip()

    # Override if very short or contains direct factual question keywords
    simple_keywords = ["how", "when", "where", "what", "who", "is", "can", "does"]
    if len(prompt.split()) < 10 and any(word in prompt for word in simple_keywords):
        return "simple"

    # If explicitly labeled as factual or basic by classifier
    simple_types = ["simple_question", "factual", "default", "lookup"]
    if prompt_type in simple_types:
        return "simple"

    # Otherwise, treat as full critique
    return "full_pipeline"
