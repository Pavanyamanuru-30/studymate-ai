"""Tests for the LLM wrapper module."""

import os
from unittest.mock import patch, MagicMock

import pytest

from utils.llm import get_gemini_response


class TestGetGeminiResponse:
    """Test suite for get_gemini_response()."""

    # ── API key validation ───────────────────────────────────

    def test_raises_error_when_api_key_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                get_gemini_response("test prompt")

    def test_raises_error_when_api_key_is_placeholder(self):
        with patch.dict(
            os.environ, {"GEMINI_API_KEY": "paste_your_api_key_here"}
        ):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                get_gemini_response("test prompt")

    def test_raises_error_when_api_key_is_empty(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                get_gemini_response("test prompt")

    # ── Successful API call (mocked) ────────────────────────

    @patch("utils.llm.genai.Client")
    def test_returns_response_text(self, mock_client_class):
        """Verify the function returns the response text from the API."""
        # Set up mock chain: Client() → client.models.generate_content() → response.text
        mock_response = MagicMock()
        mock_response.text = "This is a summary of the notes."

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-123"}):
            result = get_gemini_response("Summarize these notes")

        assert result == "This is a summary of the notes."

    @patch("utils.llm.genai.Client")
    def test_passes_correct_model(self, mock_client_class):
        """Verify the function uses the correct Gemini model."""
        mock_response = MagicMock()
        mock_response.text = "response"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-123"}):
            get_gemini_response("test prompt")

        # Check the model argument
        call_kwargs = mock_client.models.generate_content.call_args
        assert call_kwargs.kwargs["model"] == "gemini-2.0-flash"

    @patch("utils.llm.genai.Client")
    def test_passes_prompt_as_contents(self, mock_client_class):
        """Verify the function sends the prompt to the API."""
        mock_response = MagicMock()
        mock_response.text = "response"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-123"}):
            get_gemini_response("My specific prompt")

        call_kwargs = mock_client.models.generate_content.call_args
        assert call_kwargs.kwargs["contents"] == "My specific prompt"

    # ── Error propagation ────────────────────────────────────

    @patch("utils.llm.genai.Client")
    def test_propagates_api_error(self, mock_client_class):
        """Verify API errors are propagated to the caller."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception(
            "API rate limit exceeded"
        )
        mock_client_class.return_value = mock_client

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key-123"}):
            with pytest.raises(Exception, match="API rate limit exceeded"):
                get_gemini_response("test prompt")
