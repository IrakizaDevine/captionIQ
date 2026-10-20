from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .errors import ApiError, api_error_handler
from .routes.captions import router as captions_router

settings = get_settings()

app = FastAPI(title="Caption IQ API")
app.add_exception_handler(ApiError, api_error_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(captions_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
