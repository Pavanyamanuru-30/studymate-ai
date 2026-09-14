from config import MIN_INPUT_LENGTH


def validate_input(text: str) -> tuple[bool, str]:
    """
    Validate student input text before sending it to the LLM.

    Checks:
        1. Input is not empty or whitespace-only.
        2. Input meets the minimum length threshold (from config).

    Returns:
        A tuple of (is_valid, error_message).
        If is_valid is True, error_message will be an empty string.
    """
    if not text or not text.strip():
        return False, "⚠️ Please enter some text before submitting."

    if len(text.strip()) < MIN_INPUT_LENGTH:
        return False, (
            f"⚠️ Your input is too short. Please enter at least "
            f"{MIN_INPUT_LENGTH} characters for meaningful results."
        )

    return True, ""
