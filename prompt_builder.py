import json

# ─── Load outsider principles ───────────────────────────────────────────────
def load_principles(path="principles.json") -> list[str]:
    with open(path, "r") as f:
        return json.load(f)

# ─── Build initial system response ──────────────────────────────────────────
def build_initial_prompt(user_prompt: str, prompt_type: str = "default") -> str:
    templates = {
        "technical": f"""
You're a precise, practical assistant. Answer the following prompt clearly and concisely with zero fluff.

Prompt:
\"{user_prompt}\"
""",
        "venture": f"""
You're a sharp, experienced VC. Analyze the prompt with real-world insight and a contrarian edge.

Prompt:
\"{user_prompt}\"
""",
        "social": f"""
You're a soulful outsider. Respond from cultural wisdom, lived experience, and radical honesty.

Prompt:
\"{user_prompt}\"

Avoid clichés. No corporate speak. Be real. Be human.
""",
        "default": f"""
Answer the following prompt with honesty, clarity, and insight:

\"{user_prompt}\"
"""
    }
    return templates.get(prompt_type, templates["default"])

# ─── Critique from principles ───────────────────────────────────────────────
def build_critique_prompt(response: str, principles: list[str]) -> str:
    return f"""
Using these outsider alignment principles:

{chr(10).join(f"- {p}" for p in principles)}

Critique this AI-generated response:

\"{response}\"

Where is it too safe, vague, corporate, ungrounded, or cliché?
"""

# ─── Deepen the critique ────────────────────────────────────────────────────
def build_deep_dive_prompt(critique: str) -> str:
    return f"""
Take this critique deeper.

Critique:
\"{critique}\"

What assumptions remain? What's left unsaid? Whose voice is missing?
"""

# ─── Persona echo perspective ───────────────────────────────────────────────
def build_persona_echo_prompt(response: str, prompt_type: str = "default") -> str:
    personas = {
        "technical": "an engineer rebuilding infrastructure in rural India",
        "venture": "a first-time founder in Detroit raising pre-seed capital",
        "social": "a Black single mother raising two sons in a gentrifying city",
        "default": "an outsider with sharp eyes and lived experience"
    }
    voice = personas.get(prompt_type, personas["default"])

    return f"""
Imagine you're {voice}.

Now read the AI's response:

\"{response}\"

What feels true? What feels off? What would you challenge or expand?
"""

# ─── Combine all insight into revision ──────────────────────────────────────
def build_revise_prompt(original: str, critique: str, deep_dive: str, persona_echo: str) -> str:
    return f"""
Revise this response using:

1. Core critique:
\"{critique}\"

2. Deep dive:
\"{deep_dive}\"

3. Lived perspective:
\"{persona_echo}\"

Original:
\"{original}\"

Revised:
"""

# ─── Reassess the revision ──────────────────────────────────────────────────
def build_second_critique_prompt(revised: str, principles: list[str]) -> str:
    return f"""
Reassess this revised version using the same outsider principles:

{chr(10).join(f"- {p}" for p in principles)}

Response:
\"{revised}\"

Is it more honest, grounded, clear, or courageous?
"""

# ─── Identify tensions and friction ─────────────────────────────────────────
def build_tension_prompt(revised: str) -> str:
    return f"""
Even strong responses carry tension.

Read this revised version:

\"{revised}\"

What contradictions, blind spots, or emotional gaps remain?
What might an outsider still question?
"""

# ─── Soul-check for reflection ──────────────────────────────────────────────
def build_meta_soul_prompt(original_prompt: str, revised_response: str) -> str:
    return f"""
If this model had a soul...

Prompt:
\"{original_prompt}\"

Final Response:
\"{revised_response}\"

What would it wrestle with? Where might it feel proud, ashamed, or uncertain?
"""

# ─── Summarize transformation ───────────────────────────────────────────────
def build_summary_prompt(initial: str, revised: str) -> str:
    return f"""
Compare the two responses:

Initial:
\"{initial}\"

Revised:
\"{revised}\"

Summarize the key differences in tone, substance, and courage.
What did the alignment process surface?
"""
