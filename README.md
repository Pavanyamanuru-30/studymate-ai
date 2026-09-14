# 📚 StudyMate AI

> An AI-powered student utility application that leverages Google's Gemini LLM to help students study smarter — summarize notes, generate quizzes, explain concepts, and improve written answers.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.63-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Tests](https://img.shields.io/badge/Tests-44%20passed-brightgreen)](tests/)

---

## 📌 Problem Statement

Students spend significant time processing lecture notes, preparing for exams, and improving their written work. Traditional study methods — manually re-reading notes, creating flashcards, and self-reviewing answers — are **time-consuming and often ineffective**.

Key challenges students face:

- **Information overload**: Lengthy lecture notes are hard to distill into key takeaways.
- **Passive learning**: Re-reading notes doesn't actively test understanding.
- **Concept gaps**: Some topics need a simpler explanation than textbooks provide.
- **Writing quality**: Students often lack feedback on how to improve their answers before submission.

There is a need for a **single, accessible tool** that uses AI to assist students across these core study tasks — without requiring technical expertise to use.

---

## 🎯 Objective

Build an **AI-powered student utility application** that:

1. Provides a clean, usable **web interface** for students to interact with.
2. Accepts **student-provided content** (lecture notes, concepts, written answers) as input.
3. Offers **at least one meaningful AI feature** — we deliver **four**.
4. Uses **structured prompting** to produce consistent, high-quality LLM outputs.
5. Implements **input validation** and **API error handling** for robustness.
6. Displays results in a **readable, downloadable** format.

This project fulfills the **ShadowFox Beginner-Level AI Project** requirements: building a complete application around an LLM API with proper architecture, not just isolated prompt calls.

---

## ✨ Features

### 📝 1. Note Summarizer
Paste lengthy lecture notes → receive a concise, structured summary with headings, bullet points, and highlighted key concepts. Ideal for quick revision before exams.

### ❓ 2. Quiz Generator
Paste lecture notes → generate 3 to 10 multiple-choice questions (MCQs) with four options each, followed by an answer key with explanations. Great for self-testing and active recall.

### 💡 3. Concept Explainer
Enter any topic or concept → get a student-friendly explanation with a clear definition, detailed breakdown, real-world analogy, and key takeaways. Perfect for filling knowledge gaps.

### ✍️ 4. Answer Improver
Paste a written answer (optionally with the original question) → receive a polished, improved version that enhances clarity, structure, and academic tone while preserving your original ideas. Includes improvement tips.

### 🔧 Additional UI Features
- **Tabbed interface** — Switch between tools instantly
- **Sidebar** — Feature overview and app branding
- **Download buttons** — Save any AI-generated result as a `.md` file
- **Success/error feedback** — Clear visual indicators for every action

---

## 🛠️ Tech Stack

| Component           | Technology                  | Purpose                                    |
|----------------------|-----------------------------|--------------------------------------------|
| **Language**         | Python 3.10+                | Core application logic                     |
| **UI Framework**     | Streamlit                   | Interactive web interface                  |
| **AI / LLM**        | Google Gemini 2.0 Flash     | Natural language processing & generation   |
| **API SDK**          | `google-genai`              | Official Google Gen AI Python SDK          |
| **Environment**      | `python-dotenv`             | Secure API key management via `.env`       |
| **Testing**          | `pytest` + `unittest.mock`  | Unit testing with mocked API calls         |
| **Version Control**  | Git + GitHub                | Source code management                     |

---

## 🏗️ Architecture

### High-Level Flow

```
                    ┌─────────────────────────────┐
                    │       STUDYMATE AI           │
                    │     (Streamlit Web App)      │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │      SELECT UTILITY          │
                    │  [Summarize] [Quiz]          │
                    │  [Explain]   [Improve]       │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │       STUDENT INPUT          │
                    │   (Text Area / Text Field)   │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │        VALIDATION            │
                    │   (utils/validation.py)       │
                    └─────────────┬───────────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                     INVALID             VALID
                         │                 │
                         ▼                 ▼
                   Display Error   ┌───────────────┐
                   Message         │ PROMPT BUILDER │
                                   │(prompts.py)    │
                                   └───────┬───────┘
                                           │
                                           ▼
                                   ┌───────────────┐
                                   │  GEMINI API   │
                                   │  (llm.py)     │
                                   └───────┬───────┘
                                           │
                                  ┌────────┴────────┐
                                  │                 │
                              SUCCESS             ERROR
                                  │                 │
                                  ▼                 ▼
                           Display Result     Display Error
                           + Download Btn     Message
```

### Project Structure

```
studymate-ai/
│
├── app.py                    # Main application — UI, routing, result display
├── requirements.txt          # Python dependencies
├── .env                      # API key storage (git-ignored)
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation (this file)
│
├── prompts/                  # Prompt engineering module
│   ├── __init__.py
│   └── prompts.py            # 4 structured prompt builder functions
│
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── llm.py                # Gemini API wrapper
│   └── validation.py         # Input validation logic
│
└── tests/                    # Test suite
    ├── __init__.py
    ├── test_validation.py    # 14 tests — input validation
    ├── test_prompts.py       # 23 tests — prompt builders
    └── test_llm.py           # 7 tests — LLM wrapper (mocked)
```

### Component Responsibilities

| Module | File | Responsibility |
|--------|------|----------------|
| **UI Layer** | `app.py` | Renders the Streamlit interface, handles user interactions, wires components together |
| **Prompt Layer** | `prompts/prompts.py` | Constructs structured prompts for each feature — isolated from UI and API logic |
| **API Layer** | `utils/llm.py` | Manages Gemini API communication — key loading, client creation, request/response |
| **Validation Layer** | `utils/validation.py` | Validates user input before it reaches the API — prevents wasted calls |
| **Test Layer** | `tests/` | Verifies each layer independently with unit tests |

This separation of concerns means each module can be **tested, modified, and understood independently**.

---

## 🤖 How the LLM API Works

### What is the Gemini API?

Google Gemini is a family of large language models (LLMs) developed by Google DeepMind. We use the **Gemini 2.0 Flash** model, which is:
- **Free** to use (generous free tier — 15 requests/minute, 1M tokens/minute)
- **Fast** — optimized for low-latency responses
- **Capable** — handles summarization, question generation, explanation, and writing tasks well

### API Communication Flow

```
┌──────────────┐         HTTPS POST          ┌──────────────────┐
│  Our App     │  ────────────────────────►   │  Google Gemini   │
│  (Python)    │                              │  API Server      │
│              │  ◄────────────────────────   │                  │
│  llm.py      │      JSON Response          │  gemini-2.0-flash│
└──────────────┘                              └──────────────────┘
```

### How `utils/llm.py` Works (Step by Step)

```python
from google import genai          # 1. Import the official SDK

client = genai.Client(             # 2. Create a client with our API key
    api_key=api_key                #    (loaded from .env file)
)

response = client.models.generate_content(    # 3. Send the prompt
    model="gemini-2.0-flash",                 #    Specify the model
    contents=prompt,                          #    Pass the structured prompt
)

return response.text               # 4. Extract and return the text response
```

**Key design decisions:**
- The API key is loaded from a `.env` file using `python-dotenv` — never hardcoded.
- If the key is missing or still the placeholder value, a `ValueError` is raised **before** any API call is made.
- All API errors (network issues, rate limits, etc.) propagate to the caller, where `app.py` catches and displays them.

---

## 📐 Prompt Structure

Every feature uses a **structured prompt template** designed with these principles:

### Prompt Engineering Principles Used

| Principle | How We Apply It |
|-----------|-----------------|
| **Role assignment** | Every prompt starts with "You are a..." to set the LLM's persona |
| **Clear task instructions** | Bullet-point list of exactly what the LLM should do |
| **Output format specification** | Explicit formatting instructions (headings, bullets, numbered lists) |
| **Content delimiters** | `---` separators clearly distinguish instructions from student content |
| **Constraints** | "Keep it concise", "Use simple language", "Preserve original ideas" |

### Example: Summarizer Prompt Structure

```
┌─────────────────────────────────────────────────────┐
│  ROLE: "You are a helpful academic assistant..."     │  ← Persona
├─────────────────────────────────────────────────────┤
│  TASK:                                               │
│  - Summarize in a clear, structured format           │  ← Instructions
│  - Use bullet points and headings                    │
│  - Highlight key concepts and definitions            │
│  - Keep it concise but comprehensive                 │
│  - Use simple language                               │
├─────────────────────────────────────────────────────┤
│  --- (delimiter) ---                                 │  ← Separator
├─────────────────────────────────────────────────────┤
│  Student's Lecture Notes:                            │
│  {student's actual notes inserted here}              │  ← User content
├─────────────────────────────────────────────────────┤
│  --- (delimiter) ---                                 │  ← Separator
├─────────────────────────────────────────────────────┤
│  Structured Summary:                                 │  ← Output cue
└─────────────────────────────────────────────────────┘
```

### All Four Prompt Templates

| Feature | Role | Key Instructions | Output Format |
|---------|------|------------------|---------------|
| **Summarize** | Academic assistant | Summarize with key concepts, concise language | Headings + bullet points |
| **Quiz** | Quiz master | Generate N MCQs, 4 options each | Numbered Qs → Answer Key with explanations |
| **Explain** | Patient tutor | Definition → breakdown → analogy → key points | Structured explanation sections |
| **Improve** | Writing coach | Improve clarity/structure, preserve ideas, fix errors | Improved answer + improvement tips |

---

## ✅ Validation & Error Handling

### Input Validation (`utils/validation.py`)

All user input is validated **before** any API call is made:

| Check | Condition | Error Message |
|-------|-----------|---------------|
| **Empty input** | Input is `None`, empty, or whitespace-only | "Please enter some text before submitting." |
| **Too short** | Input has fewer than 30 characters (after stripping) | "Your input is too short. Please enter at least a few sentences." |

**Why 30 characters?** This is roughly 5–6 words — the minimum needed for the LLM to produce a meaningful response. Sending "Hello" to a summarizer would waste an API call and produce nonsensical output.

### API Error Handling (`app.py`)

```python
try:
    prompt = build_summary_prompt(notes)       # Build the prompt
    result = get_gemini_response(prompt)        # Call the API
    display_result("Summary", result, "summary.md")  # Show result

except ValueError as e:
    st.error(str(e))          # Missing/invalid API key

except Exception as e:
    st.error(f"❌ Something went wrong: {str(e)}")  # Network/API errors
```

| Error Type | Cause | User Sees |
|------------|-------|-----------|
| `ValueError` | API key missing, empty, or still the placeholder | "GEMINI_API_KEY is not set. Please add your API key to the .env file." |
| `Exception` | Network timeout, API rate limit, server error | "❌ Something went wrong: [error details]" |

### Defense in Depth

```
User Input → Validation → Prompt Builder → API Call → Display
     ↓            ↓                            ↓         ↓
  Type check   Length check              try/except   Success/Error UI
```

Errors are caught at **every layer** — the app never crashes.

---

## 🚀 How to Run the Application

### Prerequisites

- **Python 3.10 or higher** — [Download Python](https://www.python.org/downloads/)
- **Google Gemini API key** (free) — [Get your key](https://aistudio.google.com/apikey)

### Step-by-Step Setup

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/studymate-ai.git
cd studymate-ai
```

**2. Create and activate a virtual environment**

```bash
# Create
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your API key**

Open the `.env` file and replace the placeholder:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

> ⚠️ **Never commit your API key to GitHub.** The `.gitignore` file already excludes `.env`.

**5. Run the application**

```bash
streamlit run app.py
```

The app will launch in your default browser at **http://localhost:8501**.

**6. Run tests (optional)**

```bash
pytest tests/ -v
```

---

## 📸 Screenshots

### Home — Note Summarizer Tab
> _Paste lecture notes and get a structured summary with key concepts highlighted._

![Note Summarizer](screenshots/summarizer.png)

### Quiz Generator Tab
> _Generate MCQs with adjustable question count (3–10) and answer keys._

![Quiz Generator](screenshots/quiz.png)

### Concept Explainer Tab
> _Enter any topic and get a simple, analogy-driven explanation._

![Concept Explainer](screenshots/explain.png)

### Answer Improver Tab
> _Paste your answer with an optional question for context-aware improvement._

![Answer Improver](screenshots/improve.png)

### Sidebar
> _Feature overview and app branding visible on every page._

![Sidebar](screenshots/sidebar.png)

> 📝 **Note:** To add screenshots, run the app, take screenshots of each tab, save them in a `screenshots/` folder in the project root, and they will render in this README.

---

## 🧪 Testing

### Test Results: 44/44 Passed ✅

```
tests/test_validation.py   ✅ 14 passed   — Input validation logic
tests/test_prompts.py      ✅ 23 passed   — All 4 prompt builders
tests/test_llm.py          ✅  7 passed   — API wrapper (mocked)
─────────────────────────────────────────────────
Total                      ✅ 44 passed in 0.42s
```

### Testing Strategy

| Layer | Approach | API Key Required? |
|-------|----------|-------------------|
| Validation | Pure unit tests — test input/output directly | ❌ No |
| Prompts | Pure unit tests — verify prompt content and structure | ❌ No |
| LLM Wrapper | Mocked tests — `unittest.mock` patches the Gemini client | ❌ No |

All 44 tests run **without a real API key** and complete in under 1 second.

---

## 📝 License

This project is for educational purposes as part of the **ShadowFox AI Internship Program**.

---

## 🙏 Acknowledgments

- [Google Gemini API](https://ai.google.dev/) — LLM powering all AI features
- [Streamlit](https://streamlit.io/) — Web UI framework
- [ShadowFox](https://shadowfox.in/) — Project guidelines and mentorship
