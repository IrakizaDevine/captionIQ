import json
import re

from ..errors import ApiError
from ..schemas import Caption

PLATFORMS = ("linkedin", "facebook_instagram", "x")


def parse_captions(response_text: str) -> dict[str, Caption]:
    candidate = response_text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", candidate, re.DOTALL | re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1)
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ApiError("AI_RESPONSE_INVALID", "The AI service returned an invalid response.", 502) from exc

    if not isinstance(payload, dict) or not all(platform in payload for platform in PLATFORMS):
        raise ApiError("AI_RESPONSE_INVALID", "The AI service returned an incomplete response.", 502)

    result: dict[str, Caption] = {}
    for platform in PLATFORMS:
        value = payload[platform]
        text = value.get("text") if isinstance(value, dict) else value
        if not isinstance(text, str) or not text.strip():
            raise ApiError("AI_RESPONSE_INVALID", "The AI service returned an invalid response.", 502)
        normalized = text.strip()
        result[platform] = Caption(text=normalized, character_count=len(normalized))
    return result
