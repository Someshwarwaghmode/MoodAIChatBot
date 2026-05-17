# 🤖 MoodBot AI Chatbot

A mood-aware AI chatbot built with **Streamlit** + **LangChain** + **Mistral AI**, featuring a sleek dark terminal UI with animated chat bubbles and switchable personality modes.

---

## ✨ Features

- 🎭 **3 Personality Modes** — Sad, Angry, or Funny — switch anytime, conversation resets automatically
- 💬 **Chat Bubble UI** — user & bot messages rendered with avatars, animations, and distinct styles
- ⚡ **Powered by Mistral AI** — uses `open-mistral-7b` via LangChain's unified model interface
- 🧠 **Full Conversation Memory** — entire message history passed to the model each turn
- 🖥️ **Dark Terminal Aesthetic** — JetBrains Mono font, glowing accents, animated status dot
- 🔒 **Secure API Key Handling** — loaded from a `.env` file, never hardcoded

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/moodbot.git
cd moodbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

> Get your free API key at [console.mistral.ai](https://console.mistral.ai)

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🗂️ Project Structure

```
moodbot/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                 # API key (create this yourself, do NOT commit)
├── .gitignore           # Excludes .env and __pycache__
└── README.md
```

---

## 🎨 UI Preview

| Mode | Personality | Accent Color |
|------|------------|--------------|
| 😢 Sad | Melancholic & empathetic | Blue `#60a5fa` |
| 😡 Angry | Blunt & frustrated | Red `#f87171` |
| 😄 Funny | Jokes & puns | Yellow `#facc15` |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [LangChain](https://langchain.com) | LLM orchestration & message management |
| [Mistral AI](https://mistral.ai) | Language model (`open-mistral-7b`) |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment variable management |

---

## ⚙️ Configuration

You can swap the model in `app.py` by changing this line:

```python
init_chat_model("open-mistral-7b", model_provider="mistralai", max_tokens=200)
```

Supported Mistral models: `open-mistral-7b`, `mistral-small-latest`, `mistral-large-latest`, etc.

---

## 🔐 .gitignore

Make sure your `.gitignore` includes:

```
.env
__pycache__/
*.pyc
.streamlit/
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

> Built with ❤️ using Streamlit + LangChain + Mistral AI
