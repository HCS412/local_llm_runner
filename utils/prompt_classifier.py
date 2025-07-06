# utils/prompt_classifier.py

from typing import Dict, List, Tuple
import re
import math

class PromptClassifier:
    """
    An enhanced rule-based prompt classifier with confidence scoring.
    Designed to be extensible, robust, and semi-semantic in behavior.
    """

    def __init__(self):
        # Keyword library for each category
        self.rules: Dict[str, List[str]] = {
            "venture": [
                "startup", "funding", "vc", "venture", "investor", "cap table", "term sheet",
                "exit", "raise", "pre-seed", "angel", "dilution", "round", "portfolio"
            ],
            "technical": [
                "ai", "code", "python", "train", "build", "prompt", "api", "token", "model",
                "embedding", "inference", "weights", "script", "debug", "compute", "hardware"
            ],
            "social": [
                "community", "identity", "race", "justice", "equity", "gentrification", "bias",
                "disparity", "culture", "inclusion", "oppression", "voice", "liberation"
            ],
            "emotional": [
                "anxious", "feel", "cope", "sad", "angry", "therapy", "lonely", "overwhelmed",
                "hurt", "grief", "healing", "trauma", "depression", "panic"
            ],
            "creative": [
                "story", "poem", "imagine", "fiction", "write", "character", "lyrics", "creative",
                "plot", "narrative", "protagonist", "world-building"
            ],
            "infrastructure": [
                "bridge", "transport", "power", "grid", "access", "rural", "legacy", "infrastructure",
                "system", "connectivity", "development", "low bandwidth"
            ],
            "education": [
                "school", "teacher", "literacy", "learn", "curriculum", "education", "student",
                "homework", "college", "textbook"
            ],
            "health": [
                "health", "illness", "doctor", "care", "hospital", "treatment", "mental",
                "diagnosis", "insurance", "access"
            ],
            "climate": [
                "climate", "water", "drought", "heat", "environment", "wildfire", "carbon",
                "resilience", "green", "pollution"
            ],
            "default": []  # fallback
        }

    def detect_prompt_type_with_confidence(self, prompt: str) -> Tuple[str, float]:
        """
        Detects category with confidence score.

        Returns:
            Tuple[str, float]: category and confidence (0.0 to 1.0)
        """
        prompt = prompt.lower()
        scores: Dict[str, float] = {}

        for category, keywords in self.rules.items():
            match_count = sum(1 for kw in keywords if re.search(rf"\\b{re.escape(kw)}\\b", prompt))
            total_keywords = len(keywords) or 1  # avoid div by zero
            scores[category] = match_count / total_keywords

        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_category, top_score = sorted_scores[0]

        # Soft fallback if score is too low
        if top_score < 0.15:
            return ("contextual_product", top_score)

        return (top_category, top_score)


# Shared instance
classifier = PromptClassifier()

def classify_prompt(prompt: str, llm_runner=None) -> str:
    """
    Public interface for classification
    
    Returns:
        str: the prompt type
    """
    category, _ = classifier.detect_prompt_type_with_confidence(prompt)
    return category

def classify_prompt_with_confidence(prompt: str) -> Tuple[str, float]:
    """
    Full access method for frontend or logging
    
    Returns:
        Tuple[str, float]: category and score
    """
    return classifier.detect_prompt_type_with_confidence(prompt)
