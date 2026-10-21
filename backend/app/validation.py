from io import BytesIO

from PIL import Image, UnidentifiedImageError

from .config import Settings
from .errors import ApiError

SUPPORTED_TYPES = {"image/jpeg", "image/png", "image/webp"}
SUPPORTED_FORMATS = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}


def validate_upload(content_type: str | None, data: bytes, settings: Settings) -> str:
    if len(data) > settings.max_upload_bytes:
        raise ApiError(
            "FILE_TOO_LARGE",
            f"Please choose a photo under {settings.max_upload_mb} MB.",
            413,
        )
    if not data:
        raise ApiError("INVALID_IMAGE", "Please choose a valid JPG, PNG, or WebP image.", 400)
    if content_type not in SUPPORTED_TYPES:
        raise ApiError("INVALID_IMAGE", "Please choose a valid JPG, PNG, or WebP image.", 400)

    try:
        with Image.open(BytesIO(data)) as image:
            image.verify()
            image_format = image.format
    except (UnidentifiedImageError, OSError):
        raise ApiError("INVALID_IMAGE", "Please choose a valid JPG, PNG, or WebP image.", 400)

    detected_type = SUPPORTED_FORMATS.get(image_format or "")
    if detected_type != content_type:
        raise ApiError("INVALID_IMAGE", "Please choose a valid JPG, PNG, or WebP image.", 400)
    return detected_type


def validate_context(context: str | None, settings: Settings) -> str:
    value = context or ""
    if len(value) > settings.max_context_chars:
        raise ApiError(
            "CONTEXT_TOO_LONG",
            f"Please keep the context under {settings.max_context_chars} characters.",
            422,
        )
    return value.strip()
