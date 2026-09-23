import base64
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from config import (
    DEFAULT_QUIZ_QUESTIONS,
    MIN_QUIZ_QUESTIONS,
    MAX_QUIZ_QUESTIONS,
    MAX_HISTORY_ITEMS,
)
from prompts.prompts import (
    build_summary_prompt,
    build_quiz_prompt,
    build_explain_prompt,
    build_improve_prompt,
)
from utils.llm import get_gemini_response
from utils.validation import validate_input


# ═════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ═════════════════════════════════════════════════════════════
#  SESSION STATE
# ═════════════════════════════════════════════════════════════
if "results" not in st.session_state:
    st.session_state.results = {}

if "history" not in st.session_state:
    st.session_state.history = []


# ═════════════════════════════════════════════════════════════
#  HELPERS
# ═════════════════════════════════════════════════════════════
def add_to_history(feature: str, icon: str, preview: str):
    """Record a query in the session history (most recent first)."""
    st.session_state.history.insert(0, {
        "feature": feature,
        "icon": icon,
        "preview": preview[:60] + ("..." if len(preview) > 60 else ""),
        "time": datetime.now().strftime("%I:%M %p"),
    })
    # Keep only the last N items
    st.session_state.history = st.session_state.history[:MAX_HISTORY_ITEMS]


def word_count(text: str) -> str:
    """Return a formatted word/character count string."""
    if not text or not text.strip():
        return ""
    words = len(text.split())
    chars = len(text)
    return f"📊 {words} words · {chars} characters"


def copy_button(text: str, key: str):
    """Render a copy-to-clipboard button using JavaScript."""
    b64 = base64.b64encode(text.encode()).decode()
    components.html(f"""
        <script>
        function copyText_{key}() {{
            const text = atob("{b64}");
            navigator.clipboard.writeText(text).then(() => {{
                const btn = document.getElementById('copyBtn_{key}');
                btn.textContent = '✅ Copied!';
                setTimeout(() => btn.textContent = '📋 Copy', 2000);
            }});
        }}
        </script>
        <button id="copyBtn_{key}" onclick="copyText_{key}()" style="
            background: rgba(124,107,255,0.06);
            border: 1.5px solid #21262D;
            border-radius: 8px;
            color: #8B949E;
            padding: 6px 18px;
            cursor: pointer;
            font-size: 13px;
            font-family: Inter, sans-serif;
            width: 100%;
            transition: all 0.25s ease;
        " onmouseover="this.style.borderColor='#7C6BFF'; this.style.color='#A78BFA'"
           onmouseout="this.style.borderColor='#21262D'; this.style.color='#8B949E'">
            📋 Copy
        </button>
    """, height=42)


def display_result(icon: str, title: str, content: str, download_name: str, key: str):
    """Render AI output in a styled card with copy + download."""
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

    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        copy_button(content, key)
    with col3:
        st.download_button(
            label="📥 Save",
            data=content,
            file_name=download_name,
            mime="text/markdown",
            use_container_width=True,
        )


def handle_submission(
    input_text: str,
    prompt_fn,
    feature_key: str,
    feature_name: str,
    feature_icon: str,
    spinner_msg: str,
    prompt_kwargs: dict | None = None,
) -> bool:
    """
    Validate → build prompt → call LLM → store result.

    This is the shared logic for all 4 tabs, eliminating
    duplicated try/except and validation blocks.
    """
    is_valid, msg = validate_input(input_text)
    if not is_valid:
        st.warning(msg, icon="⚠️")
        return False

    with st.spinner(spinner_msg):
        try:
            kwargs = prompt_kwargs or {}
            prompt = prompt_fn(input_text, **kwargs)
            result = get_gemini_response(prompt)
            st.session_state.results[feature_key] = result
            add_to_history(feature_name, feature_icon, input_text)
            st.toast(f"{feature_name} ready!", icon="✅")
            return True
        except ValueError as e:
            st.error(str(e), icon="🔑")
            return False
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}", icon="❌")
            return False


# ═════════════════════════════════════════════════════════════
#  CSS
# ═════════════════════════════════════════════════════════════
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
        background: linear-gradient(90deg, transparent, rgba(124,107,255,0.05), transparent);
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
    .feature-item strong { color: #A78BFA; }

    .history-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid #21262D;
        border-radius: 8px;
        padding: 0.55rem 0.75rem;
        margin-bottom: 0.4rem;
        font-size: 0.78rem;
        color: #8B949E;
        animation: fadeIn 0.3s ease-out;
    }
    .history-item .h-feature {
        color: #A78BFA;
        font-weight: 600;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .history-item .h-preview {
        color: #6B7280;
        margin-top: 2px;
        font-size: 0.75rem;
        line-height: 1.4;
    }
    .history-item .h-time {
        color: #484F58;
        font-size: 0.68rem;
        margin-top: 2px;
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #21262D, transparent);
        margin: 0.5rem 0 1.5rem 0;
    }
    .sidebar-footer {
        text-align: center;
        color: #484F58;
        font-size: 0.75rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #21262D;
        margin-top: 1.5rem;
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

    /* ── Section ────────────────────────────────────────── */
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

    /* ── Inputs ─────────────────────────────────────────── */
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
    .stTextArea textarea::placeholder { color: #484F58 !important; }

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

    /* ── Buttons ────────────────────────────────────────── */
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
        background: rgba(124,107,255,0.06) !important;
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
    }

    /* ── Word count ─────────────────────────────────────── */
    .word-count {
        color: #484F58;
        font-size: 0.78rem;
        text-align: right;
        margin-top: -0.5rem;
        margin-bottom: 0.75rem;
        animation: fadeIn 0.3s ease-out;
    }

    /* ── Alerts & Spinner ───────────────────────────────── */
    .stAlert { border-radius: 10px; animation: fadeIn 0.3s ease-out; }
    .stSpinner > div { animation: fadeIn 0.3s ease-out; }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════════════════════
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

    # ── Usage History ────────────────────────────────────
    st.markdown("##### Recent Activity")
    if st.session_state.history:
        for item in st.session_state.history:
            st.markdown(f"""
            <div class="history-item">
                <div class="h-feature">{item['icon']} {item['feature']}</div>
                <div class="h-preview">{item['preview']}</div>
                <div class="h-time">{item['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No activity yet — try a feature!")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("##### Tips")
    st.caption("📌  Detailed notes give better results")
    st.caption("💾  Save or copy results for later review")
    st.caption("🎯  One topic per request works best")

    st.markdown("""
    <div class="sidebar-footer">
        Built with Streamlit & Google Gemini<br>
        StudyMate AI · 2026
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  HERO
# ═════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-emoji">📚</div>
    <h1>StudyMate AI</h1>
    <p>Paste your notes. Pick a tool. Let AI do the heavy lifting.</p>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  TABS
# ═════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📝 Summarize", "❓ Quiz", "💡 Explain", "✍️ Improve", "📚 Doc Q&A"]
)

# ── Tab 1: Summarize ─────────────────────────────────────────
with tab1:
    st.markdown("")
    st.markdown('<div class="sec-title">📝 Note Summarizer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">Paste your lecture notes and get an organized summary with key concepts.</div>',
        unsafe_allow_html=True,
    )

    summary_notes = st.text_area(
        "notes", height=200, placeholder="Paste your lecture notes here...",
        key="summary_input", label_visibility="collapsed",
    )
    wc = word_count(summary_notes)
    if wc:
        st.markdown(f'<div class="word-count">{wc}</div>', unsafe_allow_html=True)

    if st.button("✨  Summarize Notes", type="primary", use_container_width=True, key="btn_sum"):
        handle_submission(
            summary_notes, build_summary_prompt,
            feature_key="summary", feature_name="Summary",
            feature_icon="📝", spinner_msg="Analyzing your notes...",
        )

    if "summary" in st.session_state.results:
        display_result("📋", "Summary", st.session_state.results["summary"], "summary.md", "sum")

# ── Tab 2: Quiz ──────────────────────────────────────────────
with tab2:
    st.markdown("")
    st.markdown('<div class="sec-title">❓ Quiz Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">Turn your notes into a practice quiz for active recall.</div>',
        unsafe_allow_html=True,
    )

    quiz_notes = st.text_area(
        "notes", height=200, placeholder="Paste the notes you want to be quizzed on...",
        key="quiz_input", label_visibility="collapsed",
    )
    wc = word_count(quiz_notes)
    if wc:
        st.markdown(f'<div class="word-count">{wc}</div>', unsafe_allow_html=True)

    num_q = st.slider(
        "Number of questions",
        MIN_QUIZ_QUESTIONS, MAX_QUIZ_QUESTIONS, DEFAULT_QUIZ_QUESTIONS,
        key="quiz_slider",
    )

    if st.button("🧠  Generate Quiz", type="primary", use_container_width=True, key="btn_quiz"):
        handle_submission(
            quiz_notes, build_quiz_prompt,
            feature_key="quiz", feature_name="Quiz",
            feature_icon="❓", spinner_msg=f"Creating {num_q} questions...",
            prompt_kwargs={"num_questions": num_q},
        )

    if "quiz" in st.session_state.results:
        display_result("📝", "Your Quiz", st.session_state.results["quiz"], "quiz.md", "quiz")

# ── Tab 3: Explain ───────────────────────────────────────────
with tab3:
    st.markdown("")
    st.markdown('<div class="sec-title">💡 Concept Explainer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">Enter any topic and get a simple explanation with examples.</div>',
        unsafe_allow_html=True,
    )

    concept = st.text_area(
        "concept", height=140,
        placeholder="e.g. What is photosynthesis?\ne.g. Explain recursion with an example\ne.g. How does TCP/IP work?",
        key="explain_input", label_visibility="collapsed",
    )
    wc = word_count(concept)
    if wc:
        st.markdown(f'<div class="word-count">{wc}</div>', unsafe_allow_html=True)

    if st.button("💡  Explain This", type="primary", use_container_width=True, key="btn_exp"):
        handle_submission(
            concept, build_explain_prompt,
            feature_key="explain", feature_name="Explanation",
            feature_icon="💡", spinner_msg="Breaking it down...",
        )

    if "explain" in st.session_state.results:
        display_result("💡", "Explanation", st.session_state.results["explain"], "explanation.md", "exp")

# ── Tab 4: Improve ───────────────────────────────────────────
with tab4:
    st.markdown("")
    st.markdown('<div class="sec-title">✍️ Answer Improver</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">Paste your written answer and get a polished version with tips.</div>',
        unsafe_allow_html=True,
    )

    question = st.text_input(
        "Original question (optional — helps improve accuracy)",
        placeholder="e.g. Explain the causes of World War I",
        key="improve_q",
    )

    answer = st.text_area(
        "answer", height=200, placeholder="Paste your written answer here...",
        key="improve_input", label_visibility="collapsed",
    )
    wc = word_count(answer)
    if wc:
        st.markdown(f'<div class="word-count">{wc}</div>', unsafe_allow_html=True)

    if st.button("✍️  Improve My Answer", type="primary", use_container_width=True, key="btn_imp"):
        handle_submission(
            answer, build_improve_prompt,
            feature_key="improve", feature_name="Improved Answer",
            feature_icon="✍️", spinner_msg="Polishing your answer...",
            prompt_kwargs={"question": question},
        )

    if "improve" in st.session_state.results:
        display_result("✍️", "Improved Answer", st.session_state.results["improve"], "improved_answer.md", "imp")


# ── Tab 5: Doc Q&A (RAG) ─────────────────────────────────────
with tab5:
    st.markdown("")
    st.markdown('<div class="sec-title">📚 Document Q&A</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-desc">Upload a PDF and ask questions directly based on its content (RAG).</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"], key="pdf_uploader")

    if uploaded_file is not None:
        if "pdf_index" not in st.session_state or st.session_state.get("pdf_name") != uploaded_file.name:
            with st.spinner("Processing document (extracting, chunking, embedding)..."):
                from utils.rag import extract_text_from_pdf, chunk_text, get_embeddings, create_faiss_index
                pdf_bytes = uploaded_file.read()
                raw_text = extract_text_from_pdf(pdf_bytes)
                if not raw_text.strip():
                    st.error("No extractable text found in this PDF.")
                else:
                    chunks = chunk_text(raw_text)
                    embeddings = get_embeddings(chunks)
                    index = create_faiss_index(embeddings)
                    
                    st.session_state["pdf_index"] = index
                    st.session_state["pdf_chunks"] = chunks
                    st.session_state["pdf_name"] = uploaded_file.name
                    st.success("Document processed and indexed successfully!")
        
        if "pdf_index" in st.session_state:
            st.markdown("##### Ask a question about your document:")
            query = st.text_input("Question", placeholder="e.g. What are the key takeaways from this paper?", key="rag_query")
            
            if st.button("🔍 Search & Answer", type="primary", use_container_width=True, key="btn_rag"):
                if not query.strip():
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Searching document and generating answer..."):
                        from utils.rag import search_index
                        from prompts.prompts import build_rag_prompt
                        from utils.llm import get_gemini_response
                        
                        retrieved_chunks = search_index(query, st.session_state["pdf_index"], st.session_state["pdf_chunks"])
                        context = "\n\n".join(retrieved_chunks)
                        
                        prompt = build_rag_prompt(query, context)
                        try:
                            answer = get_gemini_response(prompt)
                            st.session_state.results["rag"] = {"answer": answer, "context": retrieved_chunks}
                            
                            add_to_history("Doc Q&A", "📚", query)
                            st.toast("Answer generated!", icon="✅")
                        except Exception as e:
                            st.error(f"Something went wrong: {str(e)}", icon="❌")

            if "rag" in st.session_state.results:
                rag_res = st.session_state.results["rag"]
                st.markdown("### Answer")
                st.markdown(rag_res["answer"])
                
                with st.expander("🔍 View Retrieved Source Context"):
                    for i, chunk in enumerate(rag_res["context"]):
                        st.markdown(f"**Source {i+1}:**")
                        st.caption(chunk)
                        st.markdown("---")
