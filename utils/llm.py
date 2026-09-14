import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_gemini_response(prompt: str) -> str:
    """
    Send a prompt to the Gemini API and return the response text.

    Uses the new google-genai SDK (replaces the deprecated google-generativeai).

    Raises:
        ValueError: If the API key is not configured.
        Exception: If the API call fails for any reason.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "paste_your_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Please add your API key to the .env file."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text
