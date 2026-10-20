def build_prompt(context: str) -> str:
    return f"""Create one social-media caption for each platform: LinkedIn, Facebook/Instagram, and X.
Return only valid JSON with exactly these keys: linkedin, facebook_instagram, x.
Each value must be an object with a single string field named text.
Keep the captions engaging, accurate to the image, and distinct for each platform.
Additional context: {context or "No additional context provided."}
"""
