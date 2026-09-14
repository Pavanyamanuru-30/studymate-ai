def validate_input(text: str) -> tuple[bool, str]:
    """
    Validate student input text before sending it to the LLM.

    Returns:
        A tuple of (is_valid, error_message).
        If is_valid is True, error_message will be an empty string.
    """
    if not text or not text.strip():
        return False, "⚠️ Please enter some text before submitting."

    if len(text.strip()) < 30:
        return False, "⚠️ Your input is too short. Please enter at least a few sentences for a meaningful summary."

    return True, ""
