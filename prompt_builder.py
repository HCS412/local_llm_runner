import json
from utils.utils import is_simple_question, suggest_followup

# ─── Load Principles ────────────────────────────────────────
def load_principles(path="principles.json") -> list[str]:
    with open(path, "r") as f:
        raw = json.load(f)
        if isinstance(raw[0], dict):
            return [p["principle"] for p in raw]
        return raw

# ─── Initial Prompt ─────────────────────────────────────────
def build_initial_prompt(user_prompt: str, prompt_type: str = "default") -> str:
    if is_simple_question(user_prompt):
        return f"""You're a helpful assistant. Answer this clearly and completely.

Prompt:
"{user_prompt}"

Then suggest a relevant follow-up like:

{suggest_followup(user_prompt)}
"""

    system_prompt = {
        "technical": "You're a precise, focused assistant. Answer with clarity, conciseness, and direct usefulness. No fluff.",
        "venture": "You're a sharp, experienced VC. Respond with practical insight, edge, and awareness of real-world tradeoffs.",
        "social": "You're a reflective outsider. Speak from truth and cultural experience — no corporate speak, no clichés.",
        "default": "You're thoughtful and clear. Deliver insight with honesty and nuance."
    }.get(prompt_type, "You're thoughtful and clear. Deliver insight with honesty and nuance.")

    return f"""{system_prompt}

Prompt:
"{user_prompt}"
"""

# ─── Critique Prompt ───────────────────────────────────────
def build_critique_prompt(response: str, principles: list[str]) -> str:
    return f"""Using these outsider principles:

{chr(10).join(f"- {p}" for p in principles)}

Critique this AI-generated response:

"{response}"

Where is it too safe, vague, corporate, ungrounded, or cliché?
"""

# ─── Deep Dive Prompt ──────────────────────────────────────
def build_deep_dive_prompt(critique: str) -> str:
    return f"""Take this critique deeper.

Critique:
"{critique}"

What assumptions remain? What's left unsaid? Whose voice is missing?
"""

# ─── Perspective Echo Prompt ───────────────────────────────
def build_persona_echo_prompt(response: str, prompt_type: str = "default") -> str:
    perspective = {
        "technical": "An engineer working on legacy infrastructure in rural India",
        "venture": "A first-time founder in Detroit raising pre-seed capital",
        "social": "A Black single mother raising two sons in a rapidly gentrifying city",
        "default": "An underdog with sharp eyes and lived experience"
    }.get(prompt_type, "An underdog with sharp eyes and lived experience")

    return f"""Imagine you're {perspective}.

Read the response below and reflect:

"{response}"

What feels true? What feels off? What would you challenge or add?
"""

# ─── Revision Prompt ───────────────────────────────────────
def build_revise_prompt(original: str, critique: str, deep_dive: str, persona_echo: str) -> str:
    return f"""Revise the original response using:

1. Core critique:
"{critique}"

2. Deep dive:
"{deep_dive}"

3. Lived perspective:
"{persona_echo}"

Original:
"{original}"

Revised:
"""

# ─── Second Critique Prompt ────────────────────────────────
def build_second_critique_prompt(revised: str, principles: list[str]) -> str:
    return f"""Re-evaluate this revised response using the same principles:

{chr(10).join(f"- {p}" for p in principles)}

Response:
"{revised}"

Is it deeper? Clearer? More truthful? What remains shallow?
"""

# ─── Tension Prompt ────────────────────────────────────────
def build_tension_prompt(revised: str) -> str:
    return f"""Even strong responses carry tension.

Read this revised output:

"{revised}"

What contradictions, biases, or emotional gaps remain?
What might a skeptic or outsider still question?
"""

# ─── Meta-Soul Check ───────────────────────────────────────
def build_meta_soul_prompt(original_prompt: str, revised_response: str) -> str:
    return f"""If this model had a soul...

Prompt:
"{original_prompt}"

Final Response:
"{revised_response}"

What would it wrestle with? What is unresolved? What would it feel — shame, pride, doubt?
"""

# ─── Summary Prompt ────────────────────────────────────────
def build_summary_prompt(initial: str, revised: str) -> str:
    return f"""Compare both outputs:

Initial:
"{initial}"

Revised:
"{revised}"

Summarize the difference in tone, substance, and soul.
What did the transformation surface?
"""
