from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. Define the output schema using Pydantic
class CaptionResponse(BaseModel):
    linkedin: str = Field(description="Professional, insightful caption with key takeaways.")
    instagram: str = Field(description="Casual, visual caption with emojis and relevant hashtags.")
    x: str = Field(description="Punchy, concise caption under 280 characters.")

# 2. Function to invoke Gemini
def call_gemini_captions(image_bytes: bytes, user_context: str) -> CaptionResponse:
    client = genai.Client()
    
    # Define prompt instructions
    prompt = f"""
    Analyze the uploaded image and the provided context.
    Generate three targeted social media captions tailored to LinkedIn, Instagram, and X.
    
    User Context: "{user_context}"
    """

    # Call the model enforcing structured JSON output
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CaptionResponse, # Enforces strict JSON matching the model schema
            temperature=0.7,
        ),
    )

    # The SDK automatically parses the response into the Pydantic model
    return response.parsed


# app/services/prompts.py

SYSTEM_PROMPT = """You are an expert social media strategist and copywriter.

Task: Analyze the provided image alongside the user's optional context string, then write 3 platform-specific captions.

Platform Guidelines:
1. LinkedIn: Tone should be professional, thought-provoking, and industry-oriented. Structure with short paragraphs or bullet points where appropriate.
2. Instagram: Tone should be engaging, expressive, and conversational. Include relevant emojis and 3-5 high-volume hashtags at the end.
3. X (Twitter): Tone should be sharp, bold, and punchy. Maximum character limit: 280 characters. No unnecessary fluff.

Constraints:
- Use details visible in the image to make the captions specific.
- Seamlessly blend the user's provided context with the visual elements.
- Return ONLY data adhering to the required schema."""