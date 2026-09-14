# 📘 Comprehensive Project Report: StudyMate AI

**Date:** September 2026  
**Project:** Beginner AI Application (ShadowFox Internship)  
**Developed by:** Pavan Kalyan  

---

## 1. Introduction & Objectives

This document outlines the complete lifecycle, architecture, and implementation details of **StudyMate AI**. The objective was to build an AI-powered student utility application around an LLM API that fulfills the requirements of the ShadowFox Beginner-Level AI Project. 

Rather than a simple script, the goal was to create a production-ready application featuring a usable interface, structured prompting, robust error handling, and high-quality UI/UX.

---

## 2. Project Pipeline & Architecture

### High-Level Workflow Pipeline
1. **Input Stage**: The user enters text (lecture notes, concepts, or answers) via the Streamlit frontend.
2. **Pre-processing & Validation**: The application checks the input for empty strings, whitespace, and minimum character thresholds (30 characters).
3. **Prompt Engineering**: The validated text is injected into a strict, predefined prompt template that dictates the persona, task, and formatting rules for the LLM.
4. **API Execution**: The prompt is dispatched to the Google Gemini 2.0 Flash API. This layer includes automated retries (via `tenacity`) and timeout handling.
5. **Post-processing & State Management**: The response is saved to Streamlit's `session_state` to prevent data loss upon UI re-renders. The request is also logged in the user's Session History.
6. **Output Stage**: The formatted Markdown response is rendered in a custom CSS card, complete with options to Copy to Clipboard or Download as a `.md` file.

### Tech Stack Utilized
- **Frontend & Routing**: Streamlit (`streamlit`)
- **LLM Engine**: Google Gemini 2.0 Flash (`google-genai`)
- **Resilience**: `tenacity` (Retry logic)
- **Security & Config**: `python-dotenv` (Environment variable management)
- **Testing**: `pytest`, `unittest.mock`
- **Version Control**: Git

---

## 3. Development Workflow: Chronological Steps Taken

The project was executed using an agile, milestone-driven approach:

### Phase 1: Foundation (Milestones 1 & 2)
- **Environment Setup**: Created a Python virtual environment and established a `.gitignore` to protect the `.env` file containing the Gemini API key.
- **Core Modules**: Built the foundational `utils/llm.py` wrapper and `utils/validation.py`.
- **First Feature**: Implemented the Note Summarizer with a basic Streamlit UI.

### Phase 2: Feature Expansion (Milestones 3, 4, & 5)
- **UI Restructuring**: Converted the single-page app into a 4-tab interface.
- **Quiz Generator**: Added a slider to dynamically pass the number of questions to the prompt builder.
- **Concept Explainer & Answer Improver**: Added the final two utilities, incorporating optional context fields (e.g., "Original Question" for the Answer Improver).

### Phase 3: Robustness & Testing (Milestones 6 & 7)
- **Unit Testing**: Authored 44 unit tests using `pytest`.
  - Tested validation boundary conditions (e.g., exactly 29 vs 30 characters).
  - Mocked the `genai.Client` to test the LLM wrapper without consuming API quotas.
  - Verified prompt templates for required instructions and formatting cues.
- **Documentation**: Drafted a comprehensive `README.md` containing architecture diagrams and setup instructions.

### Phase 4: UI Overhaul & UX Polish (Milestone 8)
- **Custom CSS**: Overrode default Streamlit styling. Implemented a GitHub-inspired dark theme with a purple accent (`#7C6BFF`).
- **Animations**: Added `@keyframes` for hero banner shimmers, fading content (`fadeInUp`), pulsing logos, and glowing focus states on text inputs.
- **Micro-interactions**: Replaced blocking error messages with non-intrusive `st.toast` notifications.

### Phase 5: Production Refactoring (Milestone 9)
- **Session State**: Prevented data loss during tab switching by caching AI responses in `st.session_state`.
- **DRY Principle**: Abstracted the redundant validation/API-call blocks across all 4 tabs into a single `handle_submission()` function.
- **Advanced UX**: Embedded JavaScript to create a "Copy to Clipboard" button and added a live word/character counter.
- **Resilience**: Integrated `tenacity` to automatically retry API calls if Gemini experiences a transient failure.

---

## 4. Detailed Implementation Procedures

### 4.1. Prompt Engineering Strategy
Prompts are defined in `prompts/prompts.py` using a structured string interpolation approach. Every prompt adheres to a specific anatomy:
1. **Persona Assignment**: e.g., *"You are a helpful academic assistant and quiz master."*
2. **Explicit Directives**: e.g., *"Generate exactly N multiple-choice questions."*
3. **Format Enforcement**: e.g., *"Provide an Answer Key with the correct answer and a one-line explanation."*
4. **Delimiters**: User input is strictly separated from instructions using `---` to prevent prompt injection or confusion.

### 4.2. API Wrapper & Resilience (`utils/llm.py`)
To prevent the application from crashing due to network blips or rate limits, the API wrapper implements the Decorator pattern via the `tenacity` library:
```python
@retry(stop=stop_after_attempt(2), wait=wait_fixed(1.0), reraise=True)
def _call_api(client, prompt):
    # API call execution
```
This ensures the app fails gracefully only after exhausting its retry budget.

### 4.3. State Management & History
Streamlit inherently reruns the entire script from top to bottom on every user interaction. To combat this:
- **`st.session_state.results`**: A dictionary that maps feature keys (e.g., `'summary'`) to their generated markdown. The UI checks this dictionary to conditionally render results.
- **`st.session_state.history`**: A list that behaves like a stack (LIFO), recording the last 10 interactions. This is rendered in the sidebar for easy user reference.

### 4.4. Security & Configuration (`config.py` & `.env`)
- **No Hardcoding**: Magic numbers (like `MIN_INPUT_LENGTH = 30`) and model names (`gemini-2.0-flash`) were extracted to a central `config.py`.
- **Secrets Management**: The API key is strictly loaded via `os.getenv("GEMINI_API_KEY")`. An explicit check ensures the app raises a descriptive `ValueError` if the key is missing or is the default placeholder, preventing silent failures.

---

## 5. Standard Operating Procedures (SOPs) Followed

During development, the following industry-standard practices were adhered to:

1. **Modular Architecture**: Code was logically grouped into `prompts/`, `utils/`, `tests/`, and the root application, ensuring high maintainability.
2. **Don't Repeat Yourself (DRY)**: Centralized configuration, abstracted API calls, and a unified UI submission handler.
3. **Test-Driven Design (TDD) Mindset**: Edge cases (like empty strings, whitespace-only inputs, and strings just below the character limit) were identified and covered by automated tests.
4. **Graceful Degradation**: If the API fails completely, the user sees a styled error toast/alert rather than a Python traceback stack.
5. **Version Control Git Flow**: Meaningful atomic commits were made at the end of every major milestone (`git commit -m "UI overhaul: ..."`).

---

## 6. Conclusion

StudyMate AI successfully transforms from a simple script into a robust, full-stack LLM application. By combining strict prompt engineering, resilient API integration, comprehensive testing, and a highly polished UI, this project comfortably exceeds the baseline requirements for the ShadowFox Beginner-Level internship task.
