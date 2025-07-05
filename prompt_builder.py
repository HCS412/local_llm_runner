import json

def load_principles(path="principles.json") -> list[str]:
    with open(path, "r") as f:
        return json.load(f)

# 🧠 Initial prompt builder
def build_initial_prompt(user_prompt: str, prompt_type: str = "default") -> str:
    if prompt_type == "technical":
        return f"""
You're a precise, focused assistant. Answer the prompt below with clarity, conciseness, and direct usefulness. No fluff.

Prompt:
"{user_prompt}"
"""
    elif prompt_type == "venture":
        return f"""
You're a sharp, experienced VC and systems thinker. Analyze and answer this prompt with practical insight and contrarian edge.

Prompt:
"{user_prompt}"
"""
    elif prompt_type == "social":
        return f"""
You're a reflective, soulful outsider. Speak from truth, experience, and cultural wisdom.

Prompt:
"{user_prompt}"

Avoid clichés. No corporate speak. Be real. Be human.
"""
    else:
        return f"""
Answer the following prompt with honesty and insight:

"{user_prompt}"
"""

# 🔍 First critique
def build_critique_prompt(response: str, principles: list[str]) -> str:
    return f"""
Using these outsider principles:

{chr(10).join(f"- {p}" for p in principles)}

Critique this AI-generated response:

"{response}"

Where is it too safe, vague, corporate, ungrounded, or cliché?
"""

# 🕳️ Deep dive
def build_deep_dive_prompt(critique: str) -> str:
    return f"""
Take this critique deeper.

Critique:
"{critique}"

What assumptions remain? What's left unsaid? Whose voice is missing?
"""

# 🎭 Perspective echo
def build_persona_echo_prompt(response: str, prompt_type: str = "default") -> str:
    perspective = {
        "technical": "An engineer working on legacy infrastructure in rural India",
        "venture": "A first-time founder in Detroit raising pre-seed capital",
        "social": "A Black single mother raising two sons in a rapidly gentrifying city",
        "default": "An underdog with sharp eyes and lived experience"
    }.get(prompt_type, "An underdog with sharp eyes and lived experience")

    return f"""
Imagine you're {perspective}.

Read the response below and reflect:

"{response}"

What feels true? What feels off? What would you challenge or add?
"""

# 🛠️ Revise based on all insights
def build_revise_prompt(original: str, critique: str, deep_dive: str, persona_echo: str) -> str:
    return f"""
Revise the original response using:

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

# 🔁 Second critique
def build_second_critique_prompt(revised: str, principles: list[str]) -> str:
    return f"""
Re-evaluate this revised response using the same principles:

{chr(10).join(f"- {p}" for p in principles)}

Response:
"{revised}"

Is it deeper? Clearer? More truthful? What remains shallow?
"""

# 🪞 Tensions
def build_tension_prompt(revised: str) -> str:
    return f"""
Even strong responses carry tension.

Read this revised output:

"{revised}"

What contradictions, biases, or emotional gaps remain?
What might a skeptic or outsider still question?
"""

# 💀 Meta soul check
def build_meta_soul_prompt(original_prompt: str, revised_response: str) -> str:
    return f"""
If this model had a soul...

Prompt:
"{original_prompt}"

Final Response:
"{revised_response}"

What would it wrestle with? What is unresolved? What would it feel — shame, pride, doubt?
"""

# 📈 Summary
def build_summary_prompt(initial: str, revised: str) -> str:
    return f"""
Compare both outputs:

Initial:
"{initial}"

Revised:
"{revised}"

Summarize the difference in tone, substance, and soul.
What did the transformation surface?
"""
