from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_outreach(persona_dict: dict, username: str) -> str:
    prompt = f"""
You're an expert in personalized outreach strategy.

Below is a persona profile for a lead extracted from their online activity. Your job is to write a **tailored cold outreach message** that speaks to their style, values, and interests.

Guidelines:
- Start with a personalized hook referencing their interests or mindset
- Be conversational but strategic (not pushy or generic)
- Clearly communicate the value proposition
- Include a subtle call-to-action (e.g., “worth chatting?”)
- Assume you're reaching out via email or LinkedIn
- Message should be 4–6 lines max

Persona:
{persona_dict}

Output the message as plain text (no formatting or YAML).
    """

    response = model.generate_content(prompt)
    return response.text.strip()
