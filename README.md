# 📚 StudyMate AI

An **AI-powered student utility application** that helps students learn smarter using Google's Gemini LLM.

Built with **Python**, **Streamlit**, and the **Google Gemini API**.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 📝 **Summarize Notes** | Paste lecture notes → get a concise, structured summary with key concepts highlighted |
| ❓ **Generate Quiz** | Paste notes → generate 3–10 MCQs with answer keys and explanations |
| 💡 **Explain a Concept** | Enter any topic → get a simple explanation with analogies and key takeaways |
| ✍️ **Improve an Answer** | Paste your written answer → get a polished, improved version with tips |

---

## 🏗️ Architecture

```
                 STUDYMATE AI
                      │
                      ▼
              ┌───────────────┐
              │ Select Utility│  (Tabs UI)
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Student Input │  (Text area / fields)
              │   Text/Notes  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   Validation  │  (utils/validation.py)
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Prompt Builder│  (prompts/prompts.py)
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Gemini API   │  (utils/llm.py)
              └───────┬───────┘
                      │
              ┌───────┴────────┐
              │                │
          Success             Error
              │                │
              ▼                ▼
       Display Answer    Display Error
       + Download btn
```

---

## 📁 Project Structure

```
studymate-ai/
│
├── app.py                  # Main Streamlit application (UI + routing)
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed to Git)
├── .gitignore              # Ignores .env, __pycache__, venv, etc.
├── README.md               # This file
│
├── prompts/
│   ├── __init__.py
│   └── prompts.py          # Structured prompt templates for all 4 features
│
└── utils/
    ├── __init__.py
    ├── llm.py              # Gemini API wrapper (google-genai SDK)
    └── validation.py       # Input validation logic
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/apikey) (free)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/studymate-ai.git
   cd studymate-ai
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Add your API key**

   Open the `.env` file and replace the placeholder:

   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

6. **Run the app**

   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`.

---

## 🧠 How It Works

### Structured Prompting

Each feature uses a carefully designed prompt template in `prompts/prompts.py`:

- **Summarizer prompt** — Instructs the LLM to produce bullet-point summaries with headings and highlighted key terms.
- **Quiz prompt** — Asks for a specific number of MCQs in a consistent format, with an answer key and explanations.
- **Explainer prompt** — Requests a definition, detailed breakdown, real-world analogy, and key takeaways.
- **Improver prompt** — Enhances clarity, structure, and academic tone while preserving the student's original ideas.

### Validation

All inputs are validated before being sent to the API:
- Empty inputs are rejected with a clear error message.
- Inputs shorter than 30 characters are rejected to ensure meaningful results.

### Error Handling

- Missing or invalid API keys are caught with a descriptive error.
- Network and API errors are caught and displayed to the user without crashing.

---

## 🛠️ Tech Stack

| Component         | Technology                |
|--------------------|--------------------------|
| Language           | Python 3.10+             |
| UI Framework       | Streamlit                |
| AI / LLM           | Google Gemini 2.0 Flash  |
| API SDK            | google-genai             |
| Environment Config | python-dotenv            |
| Version Control    | Git + GitHub             |

---

## 📸 Screenshots

> _Add screenshots of each tab here after running the app._

---

## 📝 License

This project is for educational purposes as part of the ShadowFox internship program.

---

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) for the LLM capabilities
- [Streamlit](https://streamlit.io/) for the web UI framework
- ShadowFox for the project guidelines
