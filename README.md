🔧 PromptForge
A fully local, open-source LLM prompt analysis and critique pipeline — for deep reasoning, better answers, and zero API costs.

💡 What It Does
PromptForge is a local AI-powered system that:

Classifies user prompts (simple vs. complex)

Routes them to the right LLM processing pipeline

Applies a step-by-step critique and revision process

Returns sharper, more thoughtful responses — automatically

All of this runs 100% locally using open-source models and tools like Ollama, LM Studio, and Streamlit. No API keys. No cloud dependencies.

🧱 Features
🔍 Auto classification of prompt type (simple vs full-pipeline)

🛠️ Modular pipeline with critique, persona shift, revision, and meta-reflection

⚙️ Streamlit UI for simple UX with labeled outputs and clean flow

🧠 Model-agnostic design — works with any local model (Mistral, Phi, TinyLlama, etc.)

🗂️ All outputs saved as structured markdown logs

🖼 Example Use Case
Prompt: “What should I consider before launching a SaaS business?”

PromptForge automatically:

Detects it's a strategic (complex) question

Generates a first answer

Critiques it from multiple perspectives

Revises and refines the response

Surfaces unresolved tensions

Summarizes how the final output evolved

All visible step-by-step.

🖥️ Tech Stack
Tool	Purpose
Python 3.9+	Core logic + LLM routing
Streamlit	Interactive frontend
Ollama / LM Studio	Model hosting (GGUF)
TinyLlama / Mistral / Phi	Local language models
Markdown	Output formatting & logs

🚀 Quick Start
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/HCS412/local_llm_runner.git
cd local_llm_runner
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Start the Streamlit app
bash
Copy
Edit
streamlit run app.py
4. Load a model locally
Make sure LM Studio or Ollama is running a supported model (like tinyllama, mistral, or phi).

🧪 Prompt Pipeline
The system dynamically chooses between:

Type	Description
simple	Direct factual lookup (e.g., “Who was the first president?”)
full_pipeline	Complex reasoning, reflection, or opinion-based prompts

The full pipeline includes:

Initial generation

Critique (reasoning flaws, biases)

Expansion of depth/context

Persona shift / rephrasing

Revised answer

Final critique + tension surfacing

Summary and log

📁 Directory Structure
bash
Copy
Edit
├── app.py                     # Streamlit frontend
├── main.py                    # Core CLI runner
├── utils/
│   ├── prompt_router.py       # Determines simple vs full
│   ├── utils_prompt_classifier.py # Auto prompt classifier
│   ├── formatting.py          # Markdown formatting
│   ├── __init__.py            # Imports
├── logs/                      # Run logs as .md
├── requirements.txt
├── README.md
🔧 Configuration Tips
🧠 Swap models via LM Studio or Ollama (just update in main.py)

📦 Add more critique personas by expanding principles.json

⚡ Improve performance by choosing smaller models or streamlining pipeline stages

🌐 Examples
bash
Copy
Edit
python main.py "How can I launch a startup with no funding?"
python main.py "What does it take to be a great investor?"
python main.py "Why do people still follow controversial public figures?"
📌 Roadmap
 Optional GPT-4 comparison panel

 Ability to toggle critique personas (e.g. teacher, founder, historian)

 FastAPI or local API for app integrations

 Side-by-side LLM benchmarking

 Persistent config settings and memory

🤝 Contributing
Open to ideas, PRs, and critiques — especially from:

ML builders

Prompt engineers

Educators

Philosophers

Curious hackers

📣 License
MIT License.
Build, remix, explore. Just don’t lock it behind a paywall.

