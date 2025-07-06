# utils/prompt_classifier.py

from typing import Dict, List, Optional


class PromptClassifier:
    """
    A rule-based (and future LLM-backed) prompt classifier.
    Supports easy extension and config-based updates.
    """

    def __init__(self):
        # You can later load this from a JSON/YAML config
        self.rules: Dict[str, List[str]] = {
            "venture": ["startup", "funding", "vc", "venture", "investor", "cap table", "term sheet", "deal"],
            "technical": ["ai", "code", "python", "train", "build", "prompt", "api", "token", "model"],
            "social": ["community", "identity", "race", "justice", "equity", "gentrification", "bias", "disparity"],
            "emotional": ["anxious", "feel", "cope", "sad", "angry", "therapy", "lonely", "overwhelmed"],
            "creative": ["story", "poem", "imagine", "fiction", "write", "character", "lyrics", "creative"],
            "default": []
        }

    def detect_prompt_type(self, prompt: str) -> str:
        """
        Uses keyword matching to classify the prompt into a category.

        Args:
            prompt (str): The user-provided prompt.

        Returns:
            str: One of the category labels.
        """
        prompt = prompt.lower()

        for category, keywords in self.rules.items():
            if any(term in prompt for term in keywords):
                return category

        return "default"


# Shared instance (used in app.py and main.py)
classifier = PromptClassifier()


def classify_prompt(prompt: str, llm_runner=None) -> str:
    """
    Public wrapper used in app.py or elsewhere.

    Args:
        prompt (str): The input prompt.
        llm_runner (callable, optional): For future use. If passed, allows fallback to LLM classification.

    Returns:
        str: Prompt category.
    """
    return classifier.detect_prompt_type(prompt)
