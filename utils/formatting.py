# utils/formatting.py

def format_step_header(title: str) -> str:
    """
    Format a section header for multi-step critique output.

    Args:
        title (str): The step title to format.

    Returns:
        str: Formatted header string.
    """
    return f"### 🧠 {title}\n"
