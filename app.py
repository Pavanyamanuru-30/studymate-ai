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
    /* ── Fonts ──────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ── Hide defaults ──────────────────────────────────── */
    #MainMenu, footer, header {visibility: hidden;}

    /* ── Animations ─────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 15px rgba(124, 107, 255, 0.15); }
        50%      { box-shadow: 0 0 30px rgba(124, 107, 255, 0.3); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-15px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50%      { transform: scale(1.02); }
    }

    /* ── Hero ───────────────────────────────────────────── */
    .hero {
        background: linear-gradient(135deg, #1a1333 0%, #0E1117 50%, #0d1a2d 100%);
        border: 1px solid rgba(124, 107, 255, 0.2);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: 0; left: -50%; right: -50%; bottom: 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(124, 107, 255, 0.05),
            transparent
        );
        animation: shimmer 6s ease-in-out infinite;
    }
    .hero-emoji {
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        animation: pulse 3s ease-in-out infinite;
    }
    .hero h1 {
        background: linear-gradient(135deg, #A78BFA, #7C6BFF, #60A5FA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        position: relative;
    }
    .hero p {
        color: #8B949E;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
    }

    /* ── Sidebar ────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #0D1117;
        border-right: 1px solid #21262D;
    }
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        animation: fadeIn 0.5s ease-out;
    }
    .sidebar-header .logo {
        font-size: 2.5rem;
        animation: pulse 4s ease-in-out infinite;
    }
    .sidebar-header h2 {
        background: linear-gradient(135deg, #A78BFA, #7C6BFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0.4rem 0 0.2rem 0;
    }
    .sidebar-header p {
        color: #6B7280;
        font-size: 0.82rem;
        margin: 0;
    }

    .feature-item {
        background: rgba(124, 107, 255, 0.06);
        border: 1px solid rgba(124, 107, 255, 0.1);
        border-radius: 10px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.84rem;
        color: #C9D1D9;
        transition: all 0.3s ease;
        cursor: default;
    }
    .feature-item:hover {
        background: rgba(124, 107, 255, 0.12);
        border-color: rgba(124, 107, 255, 0.3);
        transform: translateX(4px);
    }
    .feature-item strong {
        color: #A78BFA;
    }

    .sidebar-footer {
        text-align: center;
        color: #484F58;
        font-size: 0.75rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #21262D;
        margin-top: 1.5rem;
    }
    .sidebar-footer a {
        color: #6B7280;
        text-decoration: none;
    }

    /* ── Divider ────────────────────────────────────────── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #21262D, transparent);
        margin: 0.5rem 0 1.5rem 0;
    }

    /* ── Tabs ───────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #161B22;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid #21262D;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px;
        padding: 10px 18px;
        font-weight: 500;
        font-size: 0.85rem;
        color: #8B949E;
        transition: all 0.25s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #C9D1D9;
        background: rgba(124, 107, 255, 0.08);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(124, 107, 255, 0.15) !important;
        color: #A78BFA !important;
        border: 1px solid rgba(124, 107, 255, 0.3);
    }

    /* ── Section title / desc ───────────────────────────── */
    .sec-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #E6EDF3;
        margin-bottom: 0.3rem;
        animation: fadeInUp 0.4s ease-out;
    }
    .sec-desc {
        color: #8B949E;
        font-size: 0.88rem;
        margin-bottom: 1.2rem;
        line-height: 1.6;
        animation: fadeInUp 0.5s ease-out;
    }

    /* ── Text areas ─────────────────────────────────────── */
    .stTextArea textarea {
        background: #0D1117 !important;
        border: 1.5px solid #21262D !important;
        border-radius: 10px;
        color: #C9D1D9 !important;
        font-size: 0.9rem;
        padding: 14px;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #7C6BFF !important;
        box-shadow: 0 0 0 3px rgba(124, 107, 255, 0.12) !important;
    }
    .stTextArea textarea::placeholder {
        color: #484F58 !important;
    }

    /* ── Text inputs ────────────────────────────────────── */
    .stTextInput input {
        background: #0D1117 !important;
        border: 1.5px solid #21262D !important;
        border-radius: 10px;
        color: #C9D1D9 !important;
        font-size: 0.9rem;
        padding: 10px 14px;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #7C6BFF !important;
        box-shadow: 0 0 0 3px rgba(124, 107, 255, 0.12) !important;
    }

    /* ── Primary buttons ────────────────────────────────── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C6BFF, #6C5CE7) !important;
        border: none !important;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(124, 107, 255, 0.25);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 25px rgba(124, 107, 255, 0.4) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(0);
    }

    /* ── Result card ────────────────────────────────────── */
    .result-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 1rem;
        animation: fadeInUp 0.5s ease-out;
    }
    .result-card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #21262D;
    }
    .result-card-header span {
        font-size: 1.1rem;
        font-weight: 600;
        color: #A78BFA;
    }
    .result-badge {
        background: rgba(52, 211, 153, 0.1);
        color: #34D399;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        border: 1px solid rgba(52, 211, 153, 0.2);
        margin-left: auto;
    }

    /* ── Download button ────────────────────────────────── */
    .stDownloadButton button {
        background: transparent !important;
        border: 1.5px solid #21262D !important;
        border-radius: 8px;
        color: #8B949E !important;
        font-weight: 500;
        font-size: 0.82rem;
        transition: all 0.3s ease;
    }
    .stDownloadButton button:hover {
        border-color: #7C6BFF !important;
        color: #A78BFA !important;
        background: rgba(124, 107, 255, 0.08) !important;
    }

    /* ── Slider ─────────────────────────────────────────── */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: #7C6BFF;
    }

    /* ── Warning/error boxes ────────────────────────────── */
    .stAlert {
        border-radius: 10px;
        animation: fadeIn 0.3s ease-out;
    }

    /* ── Spinner ────────────────────────────────────────── */
    .stSpinner > div {
        animation: fadeIn 0.3s ease-out;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="logo">📚</div>
        <h2>StudyMate AI</h2>
        <p>AI-powered study companion</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("##### Features")
    st.markdown("""
    <div class="feature-item">📝 <strong>Summarize</strong> — Condense your notes</div>
    <div class="feature-item">❓ <strong>Quiz</strong> — Test your knowledge</div>
    <div class="feature-item">💡 <strong>Explain</strong> — Understand any concept</div>
    <div class="feature-item">✍️ <strong>Improve</strong> — Polish your answers</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("##### Tips")
    st.caption("📌  Detailed notes produce better AI results")
    st.caption("💾  Download your results for later review")
    st.caption("🎯  One topic per request works best")

    st.markdown("""
    <div class="sidebar-footer">
        Built with Streamlit & Google Gemini<br>
        StudyMate AI · 2026
    </div>
    """, unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-emoji">📚</div>
    <h1>StudyMate AI</h1>
    <p>Paste your notes. Pick a tool. Let AI do the heavy lifting.</p>
</div>
""", unsafe_allow_html=True)


# ── Helper ───────────────────────────────────────────────────
def display_result(icon: str, title: str, content: str, download_name: str):
    """Render AI output in a styled dark card with download option."""
    st.markdown(f"""
    <div class="result-card">
        <div class="result-card-header">
            <span>{icon} {title}</span>
            <div class="result-badge">✓ Generated</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("")
    col1, col2 = st.columns([3.5, 1])
    with col2:
        st.download_button(
            label="📥 Save",
            data=content,
            file_name=download_name,
            mime="text/markdown",
            use_container_width=True,
        )


# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📝 Summarize", "❓ Quiz", "💡 Explain", "✍️ Improve"]
)

# ── Tab 1: Summarize ─────────────────────────────────────────
with tab1:
    st.markdown("")
    st.markdown('<div class="sec-title">📝 Note Summarizer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">'
        "Paste your lecture notes and get an organized summary with key concepts."
        "</div>",
        unsafe_allow_html=True,
    )

    summary_notes = st.text_area(
        "notes",
        height=200,
        placeholder="Paste your lecture notes here...",
        key="summary_input",
        label_visibility="collapsed",
    )

    if st.button("✨  Summarize Notes", type="primary", use_container_width=True, key="btn_sum"):
        is_valid, msg = validate_input(summary_notes)
        if not is_valid:
            st.warning(msg, icon="⚠️")
        else:
            with st.spinner("Analyzing your notes..."):
                try:
                    result = get_gemini_response(build_summary_prompt(summary_notes))
                    st.toast("Summary ready!", icon="✅")
                    display_result("📋", "Summary", result, "summary.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")

# ── Tab 2: Quiz ──────────────────────────────────────────────
with tab2:
    st.markdown("")
    st.markdown('<div class="sec-title">❓ Quiz Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">'
        "Turn your notes into a practice quiz for active recall."
        "</div>",
        unsafe_allow_html=True,
    )

    quiz_notes = st.text_area(
        "notes",
        height=200,
        placeholder="Paste the notes you want to be quizzed on...",
        key="quiz_input",
        label_visibility="collapsed",
    )

    num_q = st.slider("Number of questions", 3, 10, 5, key="quiz_slider")

    if st.button("🧠  Generate Quiz", type="primary", use_container_width=True, key="btn_quiz"):
        is_valid, msg = validate_input(quiz_notes)
        if not is_valid:
            st.warning(msg, icon="⚠️")
        else:
            with st.spinner(f"Creating {num_q} questions..."):
                try:
                    result = get_gemini_response(build_quiz_prompt(quiz_notes, num_q))
                    st.toast("Quiz ready!", icon="✅")
                    display_result("📝", "Your Quiz", result, "quiz.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")

# ── Tab 3: Explain ───────────────────────────────────────────
with tab3:
    st.markdown("")
    st.markdown('<div class="sec-title">💡 Concept Explainer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">'
        "Enter any topic and get a simple explanation with examples."
        "</div>",
        unsafe_allow_html=True,
    )

    concept = st.text_area(
        "concept",
        height=140,
        placeholder="e.g. What is photosynthesis?\ne.g. Explain recursion with an example\ne.g. How does TCP/IP work?",
        key="explain_input",
        label_visibility="collapsed",
    )

    if st.button("💡  Explain This", type="primary", use_container_width=True, key="btn_exp"):
        is_valid, msg = validate_input(concept)
        if not is_valid:
            st.warning(msg, icon="⚠️")
        else:
            with st.spinner("Breaking it down..."):
                try:
                    result = get_gemini_response(build_explain_prompt(concept))
                    st.toast("Explanation ready!", icon="✅")
                    display_result("💡", "Explanation", result, "explanation.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")

# ── Tab 4: Improve ───────────────────────────────────────────
with tab4:
    st.markdown("")
    st.markdown('<div class="sec-title">✍️ Answer Improver</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">'
        "Paste your written answer and get a polished version with improvement tips."
        "</div>",
        unsafe_allow_html=True,
    )

    question = st.text_input(
        "Original question (optional — helps improve accuracy)",
        placeholder="e.g. Explain the causes of World War I",
        key="improve_q",
    )

    answer = st.text_area(
        "answer",
        height=200,
        placeholder="Paste your written answer here...",
        key="improve_input",
        label_visibility="collapsed",
    )

    if st.button("✍️  Improve My Answer", type="primary", use_container_width=True, key="btn_imp"):
        is_valid, msg = validate_input(answer)
        if not is_valid:
            st.warning(msg, icon="⚠️")
        else:
            with st.spinner("Polishing your answer..."):
                try:
                    result = get_gemini_response(build_improve_prompt(answer, question))
                    st.toast("Improved!", icon="✅")
                    display_result("✍️", "Improved Answer", result, "improved_answer.md")
                except ValueError as e:
                    st.error(str(e), icon="🔑")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}", icon="❌")
