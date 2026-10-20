import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _positive_float(name: str, default: float) -> float:
    value = os.getenv(name, str(default))
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


def _positive_int(name: str, default: int) -> int:
    value = os.getenv(name, str(default))
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str | None
    gemini_model: str
    max_upload_mb: int
    max_context_chars: int
    gemini_timeout_seconds: float
    allowed_origin: str

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


def get_settings() -> Settings:
    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        max_upload_mb=_positive_int("MAX_UPLOAD_MB", 5),
        max_context_chars=_positive_int("MAX_CONTEXT_CHARS", 300),
        gemini_timeout_seconds=_positive_float("GEMINI_TIMEOUT_SECONDS", 30),
        allowed_origin=os.getenv("ALLOWED_ORIGIN", "http://localhost:5173"),
    )
