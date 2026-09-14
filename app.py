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
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Font ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide Streamlit branding ────────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Hero section ───────────────────────────────────── */
    .hero-container {
        background: linear-gradient(135deg, #6C63FF 0%, #48BFE3 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.2);
    }
    .hero-title {
        color: white;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.05rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* ── Feature cards in sidebar ────────────────────────── */
    .feature-card {
        background: #F0EFFF;
        border-left: 4px solid #6C63FF;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.6rem;
        font-size: 0.88rem;
        color: #1E1E2E;
    }

    /* ── Tab styling ────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F0F2F6;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    /* ── Text areas ─────────────────────────────────────── */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1.5px solid #E0E0E0;
        font-size: 0.92rem;
        padding: 12px;
        transition: border-color 0.2s;
    }
    .stTextArea textarea:focus {
        border-color: #6C63FF;
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.15);
    }

    /* ── Result container ───────────────────────────────── */
    .result-box {
        background: white;
        border: 1px solid #E8E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .result-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #F0EFFF;
    }
    .result-header h3 {
        margin: 0;
        color: #1E1E2E;
        font-weight: 600;
    }

    /* ── Section titles ─────────────────────────────────── */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1E1E2E;
        margin-bottom: 0.25rem;
    }
    .section-desc {
        color: #6B7280;
        font-size: 0.92rem;
        margin-bottom: 1.25rem;
        line-height: 1.5;
    }

    /* ── Sidebar styling ────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FAFAFE 0%, #F5F3FF 100%);
    }
    .sidebar-brand {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .sidebar-brand h2 {
        color: #6C63FF;
        font-weight: 700;
        font-size: 1.5rem;
        margin: 0.5rem 0 0.25rem 0;
    }
    .sidebar-brand p {
        color: #6B7280;
        font-size: 0.85rem;
        margin: 0;
    }
    .sidebar-footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.78rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #E8E8F0;
        margin-top: 1.5rem;
    }

    /* ── Slider styling ─────────────────────────────────── */
    .stSlider > div > div {
        padding-top: 0.5rem;
    }

    /* ── Download button ────────────────────────────────── */
    .stDownloadButton button {
        border-radius: 8px;
        font-weight: 500;
        border: 1.5px solid #E0E0E0;
        background: white;
        transition: all 0.2s;
    }
    .stDownloadButton button:hover {
        border-color: #6C63FF;
        color: #6C63FF;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size: 3rem;">📚</div>
        <h2>StudyMate AI</h2>
        <p>Your AI study companion</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### How to use")
    st.markdown("""
    <div class="feature-card">📝 <strong>Summarize</strong> — Paste notes, get key points</div>
    <div class="feature-card">❓ <strong>Quiz</strong> — Generate practice questions</div>
    <div class="feature-card">💡 <strong>Explain</strong> — Understand any topic simply</div>
    <div class="feature-card">✍️ <strong>Improve</strong> — Polish your written answers</div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### Quick tips")
    st.info("💡 Longer, detailed notes give better results.", icon="📌")
    st.info("💡 Use the download button to save your results.", icon="💾")

    st.markdown("""
    <div class="sidebar-footer">
        Made with ❤️ using Streamlit & Gemini<br>
        StudyMate AI © 2026
    </div>
    """, unsafe_allow_html=True)

# ── Hero Section ─────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">📚 StudyMate AI</div>
    <div class="hero-subtitle">Paste. Click. Learn. — AI that helps you study smarter, not harder.</div>
</div>
""", unsafe_allow_html=True)


# ── Helper: display result ───────────────────────────────────
def display_result(icon: str, title: str, content: str, download_name: str):
    """Display AI-generated content in a styled container with download."""
    st.markdown(f"""
    <div class="result-box">
        <div class="result-header">
            <h3>{icon} {title}</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("")  # spacing
    col1, col2 = st.columns([3, 1])
    with col2:
        st.download_button(
            label="📥 Download",
            data=content,
            file_name=download_name,
            mime="text/markdown",
            use_container_width=True,
        )


# ── Tabs ─────────────────────────────────────────────────────
tab_summarize, tab_quiz, tab_explain, tab_improve = st.tabs(
    ["📝 Summarize", "❓ Quiz", "💡 Explain", "✍️ Improve"]
)

# ── Tab 1: Note Summarizer ───────────────────────────────────
with tab_summarize:
    st.markdown("")
    st.markdown('<div class="section-title">📝 Note Summarizer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        "Paste your lecture notes and get an organized, easy-to-review summary "
        "with key concepts highlighted."
        "</div>",
        unsafe_allow_html=True,
    )

    summary_notes = st.text_area(
        "Your lecture notes",
        height=220,
        placeholder="Paste your lecture notes here...\n\nTip: The more detailed your notes, the better the summary!",
        key="summary_input",
        label_visibility="collapsed",
    )

    if st.button("✨  Generate Summary", type="primary", use_container_width=True, key="btn_summarize"):
        is_valid, error_msg = validate_input(summary_notes)

        if not is_valid:
            st.warning(error_msg, icon="⚠️")
        else:
            with st.spinner("Reading your notes and creating summary..."):
                try:
                    prompt = build_summary_prompt(summary_notes)
                    result = get_gemini_response(prompt)
                    st.toast("Summary ready!", icon="✅")
                    display_result("📋", "Your Summary", result, "summary.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")

# ── Tab 2: Quiz Generator ───────────────────────────────────
with tab_quiz:
    st.markdown("")
    st.markdown('<div class="section-title">❓ Quiz Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        "Turn your notes into a practice quiz. Great for active recall "
        "and testing yourself before exams."
        "</div>",
        unsafe_allow_html=True,
    )

    quiz_notes = st.text_area(
        "Your lecture notes",
        height=220,
        placeholder="Paste the notes you want to be quizzed on...\n\nTip: Cover one topic at a time for focused questions.",
        key="quiz_input",
        label_visibility="collapsed",
    )

    col_slider, col_label = st.columns([4, 1])
    with col_slider:
        num_questions = st.slider(
            "How many questions?",
            min_value=3,
            max_value=10,
            value=5,
            step=1,
        )
    with col_label:
        st.markdown("")
        st.markdown(f"**{num_questions}** questions")

    if st.button("🧠  Generate Quiz", type="primary", use_container_width=True, key="btn_quiz"):
        is_valid, error_msg = validate_input(quiz_notes)

        if not is_valid:
            st.warning(error_msg, icon="⚠️")
        else:
            with st.spinner(f"Crafting {num_questions} questions from your notes..."):
                try:
                    prompt = build_quiz_prompt(quiz_notes, num_questions)
                    result = get_gemini_response(prompt)
                    st.toast("Quiz ready! Test yourself 🧠", icon="✅")
                    display_result("📝", "Your Quiz", result, "quiz.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")

# ── Tab 3: Concept Explainer ────────────────────────────────
with tab_explain:
    st.markdown("")
    st.markdown('<div class="section-title">💡 Concept Explainer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        "Struggling with a topic? Enter it below and get a clear explanation "
        "with real-world examples and analogies."
        "</div>",
        unsafe_allow_html=True,
    )

    concept = st.text_area(
        "What do you want explained?",
        height=150,
        placeholder="Examples:\n• What is photosynthesis and why is it important?\n• Explain recursion in programming with a simple example\n• How does the TCP/IP protocol work?",
        key="explain_input",
        label_visibility="collapsed",
    )

    if st.button("💡  Explain This", type="primary", use_container_width=True, key="btn_explain"):
        is_valid, error_msg = validate_input(concept)

        if not is_valid:
            st.warning(error_msg, icon="⚠️")
        else:
            with st.spinner("Breaking it down for you..."):
                try:
                    prompt = build_explain_prompt(concept)
                    result = get_gemini_response(prompt)
                    st.toast("Explanation ready!", icon="✅")
                    display_result("💡", "Explanation", result, "explanation.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")

# ── Tab 4: Answer Improver ──────────────────────────────────
with tab_improve:
    st.markdown("")
    st.markdown('<div class="section-title">✍️ Answer Improver</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">'
        "Paste your written answer and get a polished version with better structure, "
        "clarity, and academic tone — while keeping your ideas intact."
        "</div>",
        unsafe_allow_html=True,
    )

    question = st.text_input(
        "Original question (helps the AI give better improvements)",
        placeholder="e.g. Explain the causes and consequences of World War I",
        key="improve_question",
    )

    answer = st.text_area(
        "Your answer",
        height=220,
        placeholder="Paste your written answer here...\n\nTip: Include the question above for more context-aware improvements.",
        key="improve_input",
        label_visibility="collapsed",
    )

    if st.button("✍️  Improve My Answer", type="primary", use_container_width=True, key="btn_improve"):
        is_valid, error_msg = validate_input(answer)

        if not is_valid:
            st.warning(error_msg, icon="⚠️")
        else:
            with st.spinner("Polishing your answer..."):
                try:
                    prompt = build_improve_prompt(answer, question)
                    result = get_gemini_response(prompt)
                    st.toast("Improved answer ready!", icon="✅")
                    display_result("✍️", "Improved Answer", result, "improved_answer.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")
