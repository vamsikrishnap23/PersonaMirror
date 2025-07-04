import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

def generate_persona_from_tweets(tweets: list[str]) -> str:
    joined_tweets = "\n".join(tweets[:50])  # Limit to first 50 for prompt length

    prompt = f"""
You are an expert in behavioral analysis and marketing personas.

Based on these tweets, extract a YAML-formatted persona profile. Include:
- Age range
- Likely profession
- Key interests
- Personality traits
- Social media behavior
- Cold outreach preferences

Tweets:
{joined_tweets}
"""

    response = model.generate_content(prompt)
    return response.text.strip()

def save_lead_data(username: str, tweets: list[str], persona_yaml: str):
    folder_path = os.path.join("leads", username)
    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(folder_path, "tweets.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(tweets))

    with open(os.path.join(folder_path, "persona.yaml"), "w", encoding="utf-8") as f:
        f.write(persona_yaml)


# ✅ Example usage
if __name__ == "__main__":
    import asyncio
    from scrape_tweets import scrape_tweets

    username = "BalaInIceland"  # Change to actual username
    tweets = asyncio.run(scrape_tweets(username))

    persona_yaml = generate_persona_from_tweets(tweets)
    save_lead_data(username, tweets, persona_yaml)

    print("✅ Persona generated and saved!")
