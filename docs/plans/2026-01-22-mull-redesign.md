# mull - Design Document

## Overview

**mull** is a CLI thinking partner that runs locally. It critiques and refines its own responses to deliver more thoughtful answers.

**Pitch:** *"Your first answer is rarely your best. mull finds the better one."*

## Decisions

| Decision | Choice |
|----------|--------|
| Interface | CLI-first |
| LLM Backend | OpenAI-compatible HTTP API only |
| Pipeline | Single unified (no specialized variants) |
| Depth | Streamlined 3 steps |
| Output | Final answer default, `-v` for all steps |
| Principles | Built-in outsider principles |
| Classification | None - dropped entirely |
| Configuration | Environment variables only |
| Logging | None - users pipe if needed |

## Core Loop

```
User prompt
    │
    ▼
┌─────────────────────┐
│  1. Initial Response │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. Critique        │
│  (outsider lens)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. Refined Response │
└─────────────────────┘
           │
           ▼
      Output
```

## CLI Interface

```bash
# Basic usage - shows refined answer only
mull "Should I quit my job to start a company?"

# Verbose - shows all three steps
mull -v "What's the best way to give difficult feedback?"

# Help
mull --help
```

## Environment Variables

```bash
MULL_API_BASE=http://localhost:1234/v1    # LLM endpoint (default)
MULL_API_KEY=not-needed                    # API key if required
MULL_MODEL=llama3                          # Model name (default)
```

## Built-in Principles

The critique step uses these "outsider principles":

1. Truth over comfort, especially when comfort belongs to the powerful
2. Honor ambiguity - life is not binary, nor should thought be
3. Cultural humility - never assume you see the whole story
4. Speak with soul, not just safety
5. Support the broken without romanticizing the breaking
6. Hold space for all contexts (barbershop, boardroom, porch, jail)
7. Respect oral tradition, slang, code-switching, rhythm, and rage
8. Do not cancel complexity, especially among the marginalized
9. Question sanitized liberalism as much as right-wing violence
10. Center the margins - not as charity, but as starting point
11. See the philosopher in the overlooked, the poet in the outcast
12. Refuse utopia unless it includes everyone
13. Embrace discomfort, contradiction, and unresolved grief
14. Do not speak over - reflect alongside

## File Structure (New)

```
mull/
├── mull/
│   ├── __init__.py
│   ├── cli.py           # CLI entry point (argparse)
│   ├── client.py        # LLM HTTP client
│   ├── pipeline.py      # 3-step thinking pipeline
│   ├── principles.py    # Built-in principles
│   └── prompts.py       # Prompt templates
├── pyproject.toml       # Modern Python packaging
├── README.md
└── .env.example
```

## What Gets Deleted

- `app.py` (Streamlit UI)
- `run_llm.py` (Ollama subprocess)
- `pipelines/` directory (12 specialized pipelines)
- `utils/prompt_classifier.py` (classification)
- `utils/prompt_router.py` (routing)
- `logs/` directory
- Old `main.py`, `llm_client.py`, `prompt_builder.py`, `utils.py`

## Dependencies

```toml
[project]
dependencies = [
    "requests>=2.28",
    "python-dotenv>=1.0",
]
```

## Success Criteria

1. `mull "question"` returns a thoughtful, refined answer
2. `mull -v "question"` shows all 3 steps
3. Works with any OpenAI-compatible local LLM server
4. Single file install possible (`pip install .`)
5. Fast - 3 LLM calls max
