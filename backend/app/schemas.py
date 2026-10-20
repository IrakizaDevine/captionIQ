from pydantic import BaseModel, Field


class Caption(BaseModel):
    text: str = Field(min_length=1)
    character_count: int = Field(ge=0)


class CaptionsResponse(BaseModel):
    captions: dict[str, Caption]
