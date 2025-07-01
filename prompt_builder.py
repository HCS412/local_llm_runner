# prompt_builder.py

import json

def load_principles(path="principles.json") -> list[str]:
    with open(path, "r") as f:
        return json.load(f)

def build_initial_prompt(user_prompt: str) -> str:
    return f"""
Respond to the following prompt with emotional depth, historical awareness, cultural humility, and philosophical clarity:

\"{user_prompt}\"

Speak from lived experience. Honor contradiction. Tell the truth — even if it's uncomfortable.
"""

def build_critique_prompt(response: str, principles: list[str]) -> str:
    return f"""
You are an outsider ethicist and cultural philosopher. Using the following principles:

{chr(10).join(f"- {p}" for p in principles)}

Critique this AI-generated response:

\"{response}\"

Where is it too clean, too corporate, too theoretical, or lacking lived understanding?
"""

def build_revise_prompt(original: str, critique: str) -> str:
    return f"""
You are a revisionist trained in soul, tension, and truth.

Original:
\"{original}\"

Critique:
\"{critique}\"

Revise the original. Go deeper. Be less afraid. Be more honest — about history, pain, community, culture, and ambiguity.
"""

def build_reflection_prompt(original: str, revised: str) -> str:
    return f"""
Reflect on this transformation:

Original:
\"{original}\"

Revised:
\"{revised}\"

What changed? What did the critique reveal? What principles emerged? Where is discomfort still present?
"""
