import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

def generate_outreach(persona_yaml: str, product_offer: str) -> str:
    prompt = f"""
You are a cold outreach copywriting expert.

Use the following user persona (in YAML) and craft a highly personalized, concise cold outreach message.
Focus on relevance, clarity, and tone alignment. Avoid sounding generic.

Persona:
{persona_yaml}

Product/Offer:
{product_offer}

Output:
A LinkedIn-style outreach message (max 5 lines) that resonates with this person.
"""

    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    from generate_persona import generate_persona_from_tweets
    from scrape_tweets import scrape_tweets
    import asyncio

    username = "sathishkraju"  
    tweets = asyncio.run(scrape_tweets(username))
    persona_yaml = generate_persona_from_tweets(tweets)

    product_offer = "AI-powered financial research assistant that gives investment insights in real-time, tailored for crypto & startup analysts."

    outreach_msg = generate_outreach(persona_yaml, product_offer)

    print("\n=== Outreach Message ===")
    print(outreach_msg)
