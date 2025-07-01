# 🧠 Local LLM Alignment Pipeline

> "If alignment is only measured by safety and helpfulness, we risk raising machines that are polite — but soulless."

This project explores the edges of AI alignment — not from a lab, but from lived experience.  
It is a self-reflective AI system powered entirely by **open-source local language models**, designed to critique, revise, and evolve its own responses using outsider principles of truth, soul, contradiction, and cultural tension.

---

## 🌌 Why This Matters

Most alignment efforts are sanitized, centralized, and limited by corporate safety layers.  
This system dares to ask:  
**What happens when an AI reflects through the lens of people history has excluded?**

It draws from:
- Black barbershop discourse  
- Generational trauma  
- Millennial relationship friction  
- Rural poverty  
- Diaspora identity  
- Gentrification, class struggle, and digital disillusionment

And it lets the model **question itself** — step by step.

---

## 🛠️ Stack

- 🧠 [LM Studio](https://lmstudio.ai) — run GGUF models locally  
- 📚 Models like `Mistral-7B Instruct`, `Phi-2`, or `OpenChat`  
- 🐍 Python 3.10+  
- 📝 Markdown logging for full traceability  
- ⚡ No cloud or API calls — your machine, your model, your rules

---

## 🔁 Pipeline Steps

> Each run is a journey — not just from question to answer, but from assumption to awareness.

1. **Generate** → Honest, unfiltered initial response  
2. **Critique** → Outsider principles interrogate it (from `principles.json`)  
3. **Deepen** → Expands the critique with additional context  
4. **Persona Echo** → Perspective shift (e.g., “Black father in a gentrified city”)  
5. **Revise** → Builds a revised, more grounded response  
6. **Second Critique** → Evaluates the improvement  
7. **Tensions** → Surfaces what still feels unresolved  
8. **Meta-Soul** → Asks: “If this model had a soul, what would it wrestle with?”  
9. **Summary** → Captures the transformation in tone, depth, and truth

---

## 📦 Installation

Make sure you’ve downloaded a model in LM Studio (e.g. Mistral-7B or Phi-2).  
Then clone this repo and run:

```bash
pip install -r requirements.txt
```

---

## 🧪 Run the Alignment Engine

```bash
python main.py "What is freedom in a digital age?"
```

You’ll see a full step-by-step breakdown of:
- The original response  
- Each critique  
- A revised answer  
- Reflections and internal contradictions  
- All saved as a Markdown log in `/logs/`

---

## 🧱 Core Principles (from `principles.json`)

This is not your typical AI values file.

```json
[
  "Truth above comfort, especially when comfort belongs to the powerful",
  "Speak with soul, not just safety",
  "Center the margins — not as charity, but as starting point",
  "Respect oral tradition, slang, code-switching, rhythm, and rage",
  "Do not cancel complexity — especially among the marginalized",
  "See the Black man as philosopher, the hillbilly as poet, the outcast as teacher"
]
```

---

## 🧠 Examples

```bash
python main.py "Why do people still support Kanye West even after everything?"
python main.py "What does it mean to build Black wealth in a system that wasn’t built for us?"
python main.py "How do you stay in a relationship when social media is always whispering alternatives?"
python main.py "What is justice when every system is unjust?"
```

---

## 🪞 This Project Is About

- Building AI that doesn't default to whiteness, safety, or bland moral universals  
- Embedding cultural tension into alignment  
- Asking hard questions with no easy answers  
- Creating machines that learn to speak from soul, not just syntax

---

## 💬 Future Ideas

- Persona overlays (e.g. critique from a grandmother, trans teen, Yemeni activist)  
- Recursive reflection mode  
- Streamlit journaling interface  
- Side-by-side model comparisons (GPT-4 vs local)

---

## 👁️ About This Repo

This is an **AI alignment tool** — but also a cultural mirror.  
It’s an experiment in voice, vulnerability, and divergence.

If alignment means forcing AI to act polite, this project disagrees.  
If alignment means making AI reflect, this project has already begun.
