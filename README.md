# mull

A CLI thinking partner that critiques and refines its own responses.

*Your first answer is rarely your best. mull finds the better one.*

## What it does

You ask a question. Instead of giving you a quick answer, mull *thinks it through*:

1. **Initial response** - Answers your prompt
2. **Self-critique** - Challenges its own answer using built-in "outsider principles"
3. **Refined response** - Delivers an improved answer informed by the critique

The result: more thoughtful, more honest, less shallow responses.

## Install

```bash
git clone https://github.com/HCS412/local_llm_runner.git
cd local_llm_runner
pip install -e .
```

## Setup

Start your local LLM server, then configure:

```bash
# LM Studio (default)
export MULL_API_BASE=http://localhost:1234/v1
export MULL_MODEL=your-model-name

# Ollama
export MULL_API_BASE=http://localhost:11434/v1
export MULL_MODEL=llama3
```

Or copy `.env.example` to `.env` and edit it.

Works with LM Studio, Ollama, llama.cpp server, vLLM, or any OpenAI-compatible API.

## Usage

```bash
# Basic - shows refined answer only
mull "Should I quit my job to start a company?"

# Verbose - shows all thinking steps
mull -v "What's the best way to give difficult feedback?"

# Pipe input
echo "How do I handle a difficult conversation?" | mull
```

## The principles

mull's critique is guided by built-in "outsider principles":

- Truth over comfort, especially when comfort belongs to the powerful
- Honor ambiguity - life is not binary, nor should thought be
- Cultural humility - never assume you see the whole story
- Speak with soul, not just safety
- Center the margins - not as charity, but as starting point
- Do not speak over - reflect alongside

These give mull its distinctive voice: direct, honest, willing to sit with complexity.

## Requirements

- Python 3.9+
- A local LLM server running

## License

MIT
