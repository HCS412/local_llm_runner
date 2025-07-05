# utils/formatting.py

def format_step_header(step_name: str) -> str:
    """
    Format a step name into a stylized header.
    """
    return f"### 🧠 {step_name}\n"

def truncate_output(text: str, max_tokens: int = 500) -> str:
    """
    Truncates a string to a max number of tokens (approx. words).

    Args:
        text (str): The original string to be shortened.
        max_tokens (int): Max tokens to keep (default 500).

    Returns:
        str: Truncated text with ellipsis if needed.
    """
    words = text.split()
    if len(words) <= max_tokens:
        return text
    return " ".join(words[:max_tokens]) + " ..."
