import os
import logging
from google import genai
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

from config import MODEL_NAME, MAX_RETRIES, RETRY_DELAY_SECONDS

load_dotenv()

logger = logging.getLogger(__name__)


def _validate_api_key() -> str:
    """
    Check that a valid API key is configured.

    Raises ValueError immediately if the key is missing, empty,
    or still the placeholder — before any API call is attempted.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key.strip() == "" or api_key == "paste_your_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Please add your API key to the .env file."
        )
    return api_key


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_fixed(RETRY_DELAY_SECONDS),
    reraise=True,
)
def _call_api(client: genai.Client, prompt: str) -> str:
    """
    Send a prompt to Gemini with automatic retry on failure.

    Retries up to MAX_RETRIES times with RETRY_DELAY_SECONDS between
    attempts. If all attempts fail, the last exception is reraised.
    """
    logger.info("Sending request to %s...", MODEL_NAME)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    logger.info("Response received (%d chars).", len(response.text))
    return response.text


def get_gemini_response(prompt: str) -> str:
    """
    Send a prompt to the Gemini API and return the response text.

    Validates the API key, creates a client, and calls the API
    with automatic retry on transient failures.

    Raises:
        ValueError: If the API key is not configured.
        Exception: If the API call fails after all retry attempts.
    """
    api_key = _validate_api_key()
    client = genai.Client(api_key=api_key)

    try:
        return _call_api(client, prompt)
    except Exception as e:
        logger.error("API call failed after %d attempts: %s", MAX_RETRIES, e)
        raise
