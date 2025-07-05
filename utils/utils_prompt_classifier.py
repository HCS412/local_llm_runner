# utils/utils_prompt_classifier.py

def detect_prompt_type(prompt: str) -> str:
    """
    Naive rule-based classifier to determine prompt type.
    Replace this with LLM-based or ML-based classification later if needed.

    Args:
        prompt (str): The input prompt from the user.

    Returns:
        str: The classified type (e.g., 'technical', 'venture', 'social', or 'default')
    """

    prompt = prompt.lower()

    if any(term in prompt for term in ["startup", "funding", "vc", "venture", "investor"]):
        return "venture"
    elif any(term in prompt for term in ["ai", "code", "build", "train", "python", "model"]):
        return "technical"
    elif any(term in prompt for term in ["community", "identity", "race", "gentrification", "justice"]):
        return "social"
    else:
        return "default"
