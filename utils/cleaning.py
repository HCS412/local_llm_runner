# utils/cleaning.py

import re

def sanitize_input(text: str) -> str:
    """
    Clean and sanitize input by removing excessive whitespace,
    stripping dangerous characters, and trimming to a safe size.
    
    Args:
        text (str): Raw user input
    
    Returns:
        str: Cleaned version
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII
    return text[:2000]  # Optional: truncate to safe length
