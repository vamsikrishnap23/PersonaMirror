import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

def simulate_persona_groq(persona_yaml: str, user_msg: str, model="mixtral-8x7b-32768"):
    system_prompt = f"""
You are now role-playing the persona described below. Stay completely in character.
Reflect their tone, mindset, values, and even their emotional responses. Be assertive, sarcastic, warm, bitter—whatever fits.

Never reveal you're an AI. Respond like a real person with lived experience.

Persona:
{persona_yaml}
    """

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.85
    )

    return response.choices[0].message["content"].strip()
