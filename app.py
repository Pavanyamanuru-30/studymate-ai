import streamlit as st
from prompts.prompts import (
    build_summary_prompt,
    build_quiz_prompt,
    build_explain_prompt,
    build_improve_prompt,
)
from utils.llm import get_gemini_response
from utils.validation import validate_input

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="centered",
)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/student-male--v1.png", width=80)
    st.title("StudyMate AI")
    st.markdown(
        "An **AI-powered study assistant** that helps students "
        "learn smarter, not harder."
    )
    st.markdown("---")
    st.markdown("#### 🛠️ Features")
    st.markdown(
        """
        - 📝 **Summarize** — Condense lecture notes
        - ❓ **Quiz** — Generate practice MCQs
        - 💡 **Explain** — Understand any concept
        - ✍️ **Improve** — Polish your answers
        """
    )
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: grey; font-size: 0.85em;'>"
        "Built with Streamlit & Google Gemini<br>"
        "© 2026 StudyMate AI"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Header ───────────────────────────────────────────────────
st.title("📚 StudyMate AI")
st.caption("Paste. Click. Learn. — Your AI-powered study assistant.")
st.markdown("---")

# ── Helper: display result with download button ──────────────
def display_result(title: str, content: str, download_name: str):
    """Display AI-generated content with a download button."""
    st.markdown("---")
    st.success("✅ Generated successfully!")
    st.markdown(f"### {title}")
    st.markdown(content)
    st.download_button(
        label="📥 Download as text",
        data=content,
        file_name=download_name,
        mime="text/markdown",
    )


# ── Tabs ─────────────────────────────────────────────────────
tab_summarize, tab_quiz, tab_explain, tab_improve = st.tabs(
    ["📝 Summarize", "❓ Quiz", "💡 Explain", "✍️ Improve"]
)

# ── Tab 1: Note Summarizer ───────────────────────────────────
with tab_summarize:
    st.markdown("### 📝 Note Summarizer")
    st.markdown(
        "Paste your lecture notes below and click **Summarize** "
        "to get a concise, structured summary."
    )

    summary_notes = st.text_area(
        "Enter your lecture notes:",
        height=250,
        placeholder="Paste your lecture notes here...",
        key="summary_input",
    )

    if st.button("✨ Summarize", type="primary", use_container_width=True):
        is_valid, error_msg = validate_input(summary_notes)

        if not is_valid:
            st.error(error_msg)
        else:
            with st.spinner("Generating summary..."):
                try:
                    prompt = build_summary_prompt(summary_notes)
                    result = get_gemini_response(prompt)
                    display_result("📋 Summary", result, "summary.md")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"❌ Something went wrong: {str(e)}")

# ── Tab 2: Quiz Generator ───────────────────────────────────
with tab_quiz:
    st.markdown("### ❓ Quiz Generator")
    st.markdown(
        "Paste your lecture notes below, choose the number of questions, "
        "and click **Generate Quiz** to test your knowledge."
    )

    quiz_notes = st.text_area(
        "Enter your lecture notes:",
        height=250,
        placeholder="Paste your lecture notes here...",
        key="quiz_input",
    )

    num_questions = st.slider(
        "Number of questions:",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
    )

    if st.button("🧠 Generate Quiz", type="primary", use_container_width=True):
        is_valid, error_msg = validate_input(quiz_notes)

        if not is_valid:
            st.error(error_msg)
        else:
            with st.spinner("Generating quiz..."):
                try:
                    prompt = build_quiz_prompt(quiz_notes, num_questions)
                    result = get_gemini_response(prompt)
                    display_result("📋 Your Quiz", result, "quiz.md")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"❌ Something went wrong: {str(e)}")

# ── Tab 3: Concept Explainer ────────────────────────────────
with tab_explain:
    st.markdown("### 💡 Concept Explainer")
    st.markdown(
        "Enter a topic or concept you're struggling with, "
        "and get a clear, student-friendly explanation."
    )

    concept = st.text_area(
        "What concept do you want explained?",
        height=150,
        placeholder=(
            "e.g. What is photosynthesis?\n"
            "Explain recursion in programming\n"
            "How does TCP/IP work?"
        ),
        key="explain_input",
    )

    if st.button("💡 Explain", type="primary", use_container_width=True):
        is_valid, error_msg = validate_input(concept)

        if not is_valid:
            st.error(error_msg)
        else:
            with st.spinner("Generating explanation..."):
                try:
                    prompt = build_explain_prompt(concept)
                    result = get_gemini_response(prompt)
                    display_result("📋 Explanation", result, "explanation.md")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"❌ Something went wrong: {str(e)}")

# ── Tab 4: Answer Improver ──────────────────────────────────
with tab_improve:
    st.markdown("### ✍️ Answer Improver")
    st.markdown(
        "Paste your written answer below. Optionally include the question "
        "for better context. Get an improved, polished version back."
    )

    question = st.text_input(
        "Original question (optional):",
        placeholder="e.g. Explain the causes of World War I",
        key="improve_question",
    )

    answer = st.text_area(
        "Your answer:",
        height=250,
        placeholder="Paste your written answer here...",
        key="improve_input",
    )

    if st.button("✍️ Improve Answer", type="primary", use_container_width=True):
        is_valid, error_msg = validate_input(answer)

        if not is_valid:
            st.error(error_msg)
        else:
            with st.spinner("Improving your answer..."):
                try:
                    prompt = build_improve_prompt(answer, question)
                    result = get_gemini_response(prompt)
                    display_result(
                        "📋 Improved Answer", result, "improved_answer.md"
                    )
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"❌ Something went wrong: {str(e)}")
