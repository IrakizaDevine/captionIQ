from fastapi import APIRouter, File, Form, UploadFile

from ..config import get_settings
from ..schemas import CaptionsResponse
from ..services.gemini_client import generate_captions
from ..validation import validate_context, validate_upload

router = APIRouter()


@router.post("/generate-caption", response_model=CaptionsResponse)
async def create_captions(
    photo: UploadFile = File(...),
    context: str = Form(default=""),
) -> CaptionsResponse:
    settings = get_settings()
    data = await photo.read()
    mime_type = validate_upload(photo.filename, photo.content_type, data, settings)
    clean_context = validate_context(context, settings)
    captions = generate_captions(data, mime_type, clean_context, settings)
    return CaptionsResponse(captions=captions)
