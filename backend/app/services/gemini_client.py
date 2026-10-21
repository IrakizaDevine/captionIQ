import logging

from google import genai
from google.genai import types

from ..config import Settings
from ..errors import ApiError
from .caption_parser import parse_captions
from .prompts import build_prompt

logger = logging.getLogger(__name__)


def generate_captions(data: bytes, mime_type: str, context: str, settings: Settings):
    if not settings.gemini_api_key:
        raise ApiError("AI_NOT_CONFIGURED", "The Gemini API key is not configured.", 503)

    try:
        client = genai.Client(
            api_key=settings.gemini_api_key,
            http_options=types.HttpOptions(timeout=int(settings.gemini_timeout_seconds * 1000)),
        )
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[
                types.Part.from_bytes(data=data, mime_type=mime_type),
                build_prompt(context),
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
            ),
        )
        text = response.text
    except ApiError:
        raise
    except Exception as exc:
        logger.exception("Gemini request failed using model %s", settings.gemini_model)
        message = str(exc).lower()
        if "429" in message or "rate" in message and "limit" in message:
            raise ApiError("RATE_LIMITED", "The AI service rate limit was reached.", 429) from exc
        if getattr(exc, "code", None) == 503 or "503 unavailable" in message:
            raise ApiError(
                "AI_SERVICE_UNAVAILABLE",
                "The AI service is temporarily busy. Please try again shortly.",
                503,
            ) from exc
        raise ApiError("AI_SERVICE_ERROR", "The AI service could not generate captions.", 502) from exc

    if not text:
        raise ApiError("AI_RESPONSE_INVALID", "The AI service returned an empty response.", 502)
    return parse_captions(text)
