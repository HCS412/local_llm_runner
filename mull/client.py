"""LLM HTTP client for OpenAI-compatible APIs."""

import os
import requests
from typing import Optional

DEFAULT_API_BASE = "http://localhost:1234/v1"
DEFAULT_MODEL = "llama3"


def get_config() -> dict:
    """Load configuration from environment variables."""
    return {
        "api_base": os.getenv("MULL_API_BASE", DEFAULT_API_BASE),
        "api_key": os.getenv("MULL_API_KEY", "not-needed"),
        "model": os.getenv("MULL_MODEL", DEFAULT_MODEL),
    }


def call_llm(
    prompt: str,
    system: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """
    Call the LLM with a prompt and optional system message.

    Args:
        prompt: The user prompt
        system: Optional system message
        temperature: Sampling temperature (default 0.7)
        max_tokens: Maximum tokens in response (default 1024)

    Returns:
        The LLM's response text

    Raises:
        ConnectionError: If the LLM endpoint is unreachable
        RuntimeError: If the API returns an error
    """
    config = get_config()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api_key']}",
    }

    payload = {
        "model": config["model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(
            f"{config['api_base']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(
            f"Could not connect to LLM at {config['api_base']}. "
            "Is your local LLM server running?"
        ) from e

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"LLM API error: {response.text}") from e

    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response format: {response.text}") from e
