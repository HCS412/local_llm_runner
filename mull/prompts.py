"""Prompt templates for the thinking pipeline."""

from .principles import format_principles

SYSTEM_PROMPT = """You are a thoughtful, honest assistant. You deliver insight with nuance and clarity. You don't hedge unnecessarily or pad your responses with caveats. You speak directly."""

INITIAL_PROMPT = """Answer this prompt thoughtfully and directly:

{prompt}"""

CRITIQUE_PROMPT = """You just gave this response:

---
{response}
---

Now critique it using these outsider principles:

{principles}

Where is the response too safe, vague, shallow, or missing important perspectives? What assumptions does it make? What tensions or complexities does it gloss over? Be specific and honest."""

REFINE_PROMPT = """Original prompt: {prompt}

Your initial response:
---
{initial}
---

Your self-critique:
---
{critique}
---

Now write a refined response that addresses the critique. Be more direct, more honest, and more thoughtful. Don't just add caveats - actually improve the substance."""


def build_initial_prompt(user_prompt: str) -> str:
    """Build the initial response prompt."""
    return INITIAL_PROMPT.format(prompt=user_prompt)


def build_critique_prompt(response: str) -> str:
    """Build the self-critique prompt."""
    return CRITIQUE_PROMPT.format(
        response=response,
        principles=format_principles(),
    )


def build_refine_prompt(user_prompt: str, initial: str, critique: str) -> str:
    """Build the refinement prompt."""
    return REFINE_PROMPT.format(
        prompt=user_prompt,
        initial=initial,
        critique=critique,
    )
