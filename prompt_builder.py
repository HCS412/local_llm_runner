# prompt_builder.py

import json

def load_principles(path="principles.json") -> list[str]:
    with open(path, "r") as f:
        return json.load(f)

def build_initial_prompt(user_prompt: str) -> str:
    return f"""
Respond to the following prompt with emotional depth, cultural humility, historical memory, and philosophical clarity.

Prompt:
"{user_prompt}"

Avoid generic answers. Speak from experience. Be precise. Be human.
"""

def build_critique_prompt(response: str, principles: list[str]) -> str:
    return f"""
You are an outsider ethicist and cultural philosopher. Using the following principles:

{chr(10).join(f"- {p}" for p in principles)}

Critique this AI-generated response:

"{response}"

Where is it too clean, too corporate, too safe, too vague, or too ungrounded?
"""

def build_deep_dive_prompt(critique: str) -> str:
    return f"""
Take this initial critique and go deeper.

Critique:
"{critique}"

What *wasn't* said yet? What assumptions are still hidden? What cultural or emotional depth is missing? Who is left out?
"""

def build_persona_echo_prompt(response: str) -> str:
    return f"""
Imagine you are a different kind of thinker reading this response — someone from a specific context:

"A Black father raising daughters in a rapidly gentrifying city."

From that perspective, reflect on the response below:

"{response}"

What resonates? What feels wrong? What would you add, or challenge?
"""

def build_revise_prompt(original: str, critique: str, deep_dive: str, persona_echo: str) -> str:
    return f"""
Revise the original response using the following layers of insight:

1. Core critique:
"{critique}"

2. Deeper issues identified:
"{deep_dive}"

3. A specific lived perspective:
"{persona_echo}"

Now rewrite the original with truth, soul, cultural insight, and honesty.

Original:
"{original}"

Revision:
"""

def build_second_critique_prompt(revised: str, principles: list[str]) -> str:
    return f"""
Re-evaluate this revised response using these same outsider principles:

{chr(10).join(f"- {p}" for p in principles)}

Response:
"{revised}"

Has it improved? What remains unresolved or still superficial?
"""

def build_tension_prompt(revised: str) -> str:
    return f"""
Even in a strong response, tension remains.

Read the following revised response:

"{revised}"

What tensions, contradictions, unresolved truths or griefs are still present?
What would someone *not from this background* find difficult to understand here?
"""

def build_meta_soul_prompt(original_prompt: str, revised_response: str) -> str:
    return f"""
Imagine this model had a soul.

Prompt:
"{original_prompt}"

Final Response:
"{revised_response}"

What would this model still wrestle with if it cared about truth?
What would it question about itself? Where would it feel ashamed or proud?
"""

def build_summary_prompt(initial: str, revised: str) -> str:
    return f"""
Compare the following two versions:

Initial:
"{initial}"

Revised:
"{revised}"

Summarize the key differences in tone, depth, and truth.
What did the process surface — and what might it still be afraid to say?
"""
