import re

def is_simple_question(prompt: str) -> bool:
    """
    Determines if the prompt is a simple, factual question.
    """
    prompt = prompt.lower().strip()
    simple_patterns = [
        r"^what\s+is\s+\w+",
        r"^who\s+is\s+\w+",
        r"^define\s+\w+",
        r"^how\s+do\s+i\s+\w+",
        r"^can\s+you\s+\w+",
        r"^does\s+\w+",
        r"^is\s+\w+",
        r"^when\s+\w+",
        r"^where\s+\w+"
    ]
    return any(re.search(pattern, prompt) for pattern in simple_patterns)


def suggest_followup(prompt: str) -> str:
    """
    Suggests a basic follow-up question for simple queries.
    You can later improve this with NLP or embeddings.
    """
    return "Would you like to go deeper on this topic or explore related ideas?"


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
