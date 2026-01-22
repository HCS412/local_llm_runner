"""The 3-step thinking pipeline: Initial -> Critique -> Refine."""

from dataclasses import dataclass
from typing import Optional, Callable

from .client import call_llm
from .prompts import (
    SYSTEM_PROMPT,
    build_initial_prompt,
    build_critique_prompt,
    build_refine_prompt,
)


@dataclass
class ThinkingResult:
    """Result of the thinking pipeline."""

    prompt: str
    initial: str
    critique: str
    refined: str


def think(
    prompt: str,
    on_step: Optional[Callable[[str, str], None]] = None,
) -> ThinkingResult:
    """
    Run the 3-step thinking pipeline.

    Args:
        prompt: The user's question or prompt
        on_step: Optional callback called after each step with (step_name, content)

    Returns:
        ThinkingResult with all three stages
    """

    def notify(step: str, content: str):
        if on_step:
            on_step(step, content)

    # Step 1: Initial response
    initial = call_llm(
        build_initial_prompt(prompt),
        system=SYSTEM_PROMPT,
    )
    notify("initial", initial)

    # Step 2: Self-critique
    critique = call_llm(
        build_critique_prompt(initial),
        system="You are a sharp, honest critic. Be specific and direct.",
    )
    notify("critique", critique)

    # Step 3: Refined response
    refined = call_llm(
        build_refine_prompt(prompt, initial, critique),
        system=SYSTEM_PROMPT,
    )
    notify("refined", refined)

    return ThinkingResult(
        prompt=prompt,
        initial=initial,
        critique=critique,
        refined=refined,
    )
