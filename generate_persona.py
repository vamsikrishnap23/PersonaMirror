import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_persona(tweets: str, username: str) -> str:
    prompt = f"""
You're a world-class behavioral analyst and digital persona builder.

Below are tweets from a user named **{username}**. Read them carefully and build a highly accurate persona profile in valid **YAML format**.

Extract the following details:
- **Name**: A creative or descriptive title for this person (e.g., "Tech-Savvy Investor")
- **Age**: Estimated age range (e.g., "25-35")
- **Location**: Probable location based on context, language, culture or topics
- **Profession**: Likely profession or domain (e.g., Product Manager, Angel Investor)
- **Interests**: Based on content and repeated patterns (e.g., AI, crypto, fitness)
- **Personality Traits**: Tone, mindset, style (e.g., analytical, enthusiastic)
- **Social Media Behavior**: Style of tweeting, who they engage with, tone, hashtags
- **Cold Outreach Preference**: Best way to pitch them (tone, length, platform)

Respond with ONLY valid YAML. No code blocks, no extra text. Start your output directly with `persona:`.

Tweets:
{tweets}
    """

    response = model.generate_content(prompt)
    return response.text.strip()
