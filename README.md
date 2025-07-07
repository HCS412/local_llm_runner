🧠 PromptForge
Orchestrated Local Reasoning with LLMs
A fully local, open-source pipeline for structured prompt analysis, critique, and contextual revision. Built for thinkers, hackers, and alignment nerds.

💡 What It Does
PromptForge goes beyond basic prompting. It:

Classifies prompts based on topic, tone, and complexity

Selects dynamic reasoning personas for diverse reflection

Orchestrates a modular pipeline of critique, reframing, and revision

Surfaces tension and multiple perspectives

Returns answers that think deeper — all 100% locally

No API keys. No tracking. No cloud calls.
Just reasoning on your machine.

🔧 Why It Matters
LLMs are too often trained to be helpful, polite, and forgettable.
PromptForge helps them be critical, context-aware, and even soulful.

It’s a new kind of reasoning tool:

One that shows its work

That critiques itself

That doesn't just echo Silicon Valley defaults

And runs locally for total transparency + ownership

🧱 Key Features
Feature	Description
🧠 Prompt classifier	Auto-detects complexity, topic, tone
🔁 Pipeline orchestration	Step-by-step critique + reframe flow
🎭 Dynamic personas	Models respond as barbers, poets, technologists, etc.
📊 Confidence scoring	Know how confidently a category is chosen
🖼 Expandable Streamlit UI	Clean, card-based outputs with step labels
🧩 Model-agnostic	Works with any local LLM (TinyLLaMA, Mistral, Phi)
🗂 Logs everything	All runs saved as structured markdown for later analysis

🖥️ Tech Stack
Tool	Purpose
Python 3.9+	Core logic, classification, orchestration
Streamlit	UI frontend
Ollama / LM Studio	Local model runners (GGUF)
TinyLLaMA, Mistral, Phi	Example models
Markdown	Output formatting & logs

🖼 Example Flow
Prompt:

“What should I consider before launching a SaaS business?”

PromptForge:

Classifies as venture + complex

Chooses relevant reasoning personas

Runs a full multi-step critique pipeline

Surfaces tensions, alternative framings

Revises and finalizes

→ Returns layered insight instead of generic tips.

🚀 Quick Start
bash
Copy
Edit
git clone https://github.com/HCS412/local_llm_runner.git
cd local_llm_runner
pip install -r requirements.txt
streamlit run app.py
🧠 Be sure to have a local LLM loaded via LM Studio or Ollama (e.g. TinyLLaMA, Mistral, Phi).

⚙️ Prompt Routing
Type	Description
simple	Short, factual prompts → direct LLM response
full_pipeline	Deeper prompts → critique, personas, revisions

Full Pipeline Stages:
Initial generation

Reasoning critique

Persona reframing

Answer revision

Meta-summary

Follow-up suggestions

Markdown log output

📁 Directory Overview
bash
Copy
Edit
├── app.py                     # Streamlit frontend
├── main.py                    # CLI runner
├── utils/
│   ├── prompt_router.py       # Pipeline decision logic
│   ├── prompt_classifier.py   # Smart classification engine
│   ├── dynamic_persona_router.py # Persona selection system
│   ├── formatting.py          # Markdown cleanup
├── logs/                      # Markdown logs
├── requirements.txt
└── README.md
🧠 Config Tips
🎭 Add more personas in dynamic_persona_router.py

⚡ Run smaller models for speed, or swap for custom ones

🔄 Easily plug in sentence embeddings or OpenAI fallback

🪞 Use markdown logs to analyze model behavior over time

🌐 Example Prompts
bash
Copy
Edit
python main.py "How can I launch a startup with no funding?"
python main.py "Why do people follow controversial public figures?"
python main.py "What should I teach my kids about race and AI?"
🧭 Roadmap
 Side-by-side model comparisons (TinyLLaMA vs GPT-4)

 FastAPI server mode

 Toggle personas per run

 Memory + prompt history

 External dataset reflection

 User-defined critique stages

🤝 Contribute
We welcome:

🧠 Philosophers + prompt engineers

👩‍🔧 Builders + model tinkerers

🔬 Researchers on alignment, cognition, or bias

🧩 Creative weirdos and systems thinkers

Open a PR, issue, or idea.

🪪 License
MIT.
Build. Remix. Learn. Reflect.
Just don’t put it behind a paywall.
