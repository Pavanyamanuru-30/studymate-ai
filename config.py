"""
Central configuration for StudyMate AI.

All tunable settings live here so nothing is hardcoded
across multiple files.
"""

# ── LLM Settings ─────────────────────────────────────────────
MODEL_NAME = "gemini-2.0-flash"
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 1.0

# ── Validation Settings ──────────────────────────────────────
MIN_INPUT_LENGTH = 30

# ── App Settings ─────────────────────────────────────────────
MAX_HISTORY_ITEMS = 10
DEFAULT_QUIZ_QUESTIONS = 5
MIN_QUIZ_QUESTIONS = 3
MAX_QUIZ_QUESTIONS = 10
