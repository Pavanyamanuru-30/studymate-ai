"""Tests for the input validation module."""

from utils.validation import validate_input


class TestValidateInput:
    """Test suite for validate_input()."""

    # ── Rejection cases ──────────────────────────────────────

    def test_empty_string_is_rejected(self):
        is_valid, error = validate_input("")
        assert is_valid is False
        assert "enter some text" in error.lower() or len(error) > 0

    def test_none_is_rejected(self):
        is_valid, error = validate_input(None)
        assert is_valid is False

    def test_whitespace_only_is_rejected(self):
        is_valid, error = validate_input("     ")
        assert is_valid is False

    def test_tabs_and_newlines_only_is_rejected(self):
        is_valid, error = validate_input("\t\n\t\n")
        assert is_valid is False

    def test_too_short_input_is_rejected(self):
        is_valid, error = validate_input("Hello")
        assert is_valid is False
        assert "too short" in error.lower()

    def test_input_just_under_threshold_is_rejected(self):
        # 29 characters — just under the 30-char minimum
        is_valid, error = validate_input("a" * 29)
        assert is_valid is False

    # ── Acceptance cases ─────────────────────────────────────

    def test_input_at_threshold_is_accepted(self):
        # Exactly 30 characters
        is_valid, error = validate_input("a" * 30)
        assert is_valid is True
        assert error == ""

    def test_normal_input_is_accepted(self):
        is_valid, error = validate_input(
            "Photosynthesis is the process by which plants convert sunlight into energy."
        )
        assert is_valid is True
        assert error == ""

    def test_long_input_is_accepted(self):
        is_valid, error = validate_input("word " * 500)
        assert is_valid is True
        assert error == ""

    def test_input_with_leading_whitespace_is_accepted(self):
        # After stripping, this is > 30 chars
        is_valid, error = validate_input(
            "   This is a valid input with leading whitespace that should pass."
        )
        assert is_valid is True
        assert error == ""

    # ── Return type checks ───────────────────────────────────

    def test_returns_tuple(self):
        result = validate_input("Some valid input text for testing purposes.")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_valid_result_has_empty_error(self):
        is_valid, error = validate_input(
            "A sufficiently long input for validation."
        )
        assert is_valid is True
        assert error == ""

    def test_invalid_result_has_non_empty_error(self):
        is_valid, error = validate_input("")
        assert is_valid is False
        assert len(error) > 0
