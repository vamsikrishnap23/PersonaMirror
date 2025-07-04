import streamlit as st
import yaml
import os
import openai
import asyncio
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
from PIL import Image
from utils import (
    LEADS_DIR,
    get_user_dir,
    get_tweets_path,
    get_persona_path,
    get_outreach_path,
    sanitize_yaml_file
)

from generate_persona import generate_persona
from scrape_tweets import scrape_tweets  
from generate_outreach import generate_outreach 

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"
MODEL = "llama3-70b-8192"



st.set_page_config(page_title="Persona Builder", layout="wide")
st.title("Persona Builder")

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Build Persona", "Chat with Leads", "Find Similar Persona"])

# -------------------------
# 📊 Dashboard tab
# -------------------------
with tab1:
    st.header("View Persona")

    usernames = [d for d in os.listdir(LEADS_DIR) if os.path.isdir(os.path.join(LEADS_DIR, d))]
    selected_user = st.selectbox("Choose a username", usernames)

    if selected_user:
        persona_path = get_persona_path(selected_user)
        sanitize_yaml_file(persona_path)

        st.subheader("Persona YAML")
        with open(persona_path, "r", encoding="utf-8") as f:
            st.code(f.read(), language="yaml")

        st.subheader("Tweets")
        tweets_path = get_tweets_path(selected_user)
        if os.path.exists(tweets_path):
            with open(tweets_path, "r", encoding="utf-8") as f:
                tweets_text = f.read()
                st.text(tweets_text)
        else:
            tweets_text = ""
            st.warning("No tweets found.")

        # Show Word Cloud
        if tweets_text:
            st.subheader("Word Cloud")
            wordcloud = WordCloud(width=2400, height=1200, background_color="white", colormap="tab10").generate(tweets_text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

        st.subheader("Cold Outreach Email")
        outreach_path = get_outreach_path(selected_user)
        if os.path.exists(outreach_path):
            with open(outreach_path, "r", encoding="utf-8") as f:
                st.markdown(f"```markdown\n{f.read()}\n```")
        else:
            st.warning("No outreach email found. Generate one in the workflow tab.")


# -------------------------
# ⚙️ Workflow tab
# -------------------------

with tab2:
    st.header("Persona Workflow")

    username = st.text_input("Enter Twitter username")

    with st.expander("🔐 How to Authenticate with Your Twitter Cookies", expanded=False):
        st.markdown("### Authentication Required")
        st.info("""
        To scrape tweets securely from your own Twitter/X account, you need to provide a valid `cookies.json` file.

        #### How to Create One:
        1. Install the [**EditThisCookie** Chrome Extension](https://chromewebstore.google.com/detail/editthiscookie-v3/ojfebgpkimhlhcblbalbfjblapadhbol)
        2. Go to [x.com](https://x.com) and ensure you're logged in.
        3. Click the EditThisCookie extension icon → **Export** cookies → Save as `raw_cookies.json`
        4. Run the Python script below to clean and extract only the required fields (`auth_token`, `ct0`) for scraping.
        """)

        st.download_button(
            label="⬇Download Cookie Reformat Script",
            file_name="reformat_cookies.py",
            mime="text/x-python",
            data="""
    import json

    def extract_required_cookies(input_file='raw_cookies.json', output_file='cookies.json'):
        with open(input_file, 'r', encoding='utf-8') as f:
            browser_cookies = json.load(f)

        required_keys = ['auth_token', 'ct0']
        twikit_cookies = {}

        for cookie in browser_cookies:
            name = cookie.get('name')
            value = cookie.get('value')
            if name in required_keys:
                twikit_cookies[name] = value

        if len(twikit_cookies) != len(required_keys):
            print("Missing required cookies. Found:", list(twikit_cookies.keys()))
            print("Make sure you're logged in to Twitter/X and export cookies *after* logging in.")
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(twikit_cookies, f, indent=4)

        print(f"Reformatted cookies saved to `{output_file}`")
        print("Contents:", twikit_cookies)

    if __name__ == "__main__":
        extract_required_cookies()
    """
        )

    st.warning("⚠️ Make sure `cookies.json` is saved in the project root folder.")

    if st.button("Scrape Tweets"):
        if username:
            try:
                with st.spinner("Scraping..."):
                    tweets = asyncio.run(scrape_tweets(username))
                    user_dir = get_user_dir(username)
                    os.makedirs(user_dir, exist_ok=True)
                    with open(get_tweets_path(username), "w", encoding="utf-8") as f:
                        f.write("\n".join(tweets))
                    st.success(f"Scraped {len(tweets)} tweets.")
            except Exception as e:
                st.error(f"Scraping failed: {e}")
        else:
            st.warning("Please enter a Twitter username.")

    if st.button("Generate Persona"):
        tweets_path = get_tweets_path(username)
        if os.path.exists(tweets_path):
            with open(tweets_path, "r", encoding="utf-8") as f:
                tweets = f.read()
            persona_yaml = generate_persona(tweets, username)
            with open(get_persona_path(username), "w", encoding="utf-8") as f:
                f.write(persona_yaml)
            st.success("Persona generated.")
        else:
            st.warning("Scrape tweets first.")

    if st.button("Generate Cold Outreach"):
        persona_path = get_persona_path(username)
        if os.path.exists(persona_path):
            sanitize_yaml_file(persona_path)
            with open(persona_path, "r", encoding="utf-8") as f:
                persona = yaml.safe_load(f)

            outreach = generate_outreach(persona, username)
            with open(get_outreach_path(username), "w", encoding="utf-8") as f:
                f.write(outreach)
            st.code(outreach, language="markdown")
            st.success("Outreach generated.")
        else:
            st.warning("Generate persona first.")


with tab3:
    st.header("Chat as Persona")

    chat_user = st.selectbox("Select a persona to simulate", usernames, key="chat_user")

    if chat_user:
        persona_path = get_persona_path(chat_user)
        sanitize_yaml_file(persona_path)

        with open(persona_path, "r", encoding="utf-8") as f:
            persona_yaml = f.read()

        # Chat tone selection
        tone = st.radio("Select response style", [
            "Default",
            "Cold Outreach Mode",
            "Friendly Discussion",
            "Pitch Evaluation"
        ])

        # Conversation state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_msg = st.chat_input("You:")
        if user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})

            # Tone-specific instruction
            tone_instructions = {
                "Default": "",
                "Cold Outreach Mode": "- Prioritize concise, skeptical, ROI-focused replies.",
                "Friendly Discussion": "- Be supportive, casual, curious and polite.",
                "Pitch Evaluation": "- Respond analytically and rate the pitch's clarity and potential."
            }

            system_prompt = f"""
                You are now simulating the persona described below. Do not invent new traits, tone, or behavior — strictly follow the details provided.

                Respond as this individual would in any situation:
                - Match their **interests**, **profession**, and **communication preferences**.
                - Mirror their **tone**, even if it’s blunt, bitter, skeptical, sarcastic, overly enthusiastic, formal, or casual.
                - If their personality is confrontational or passive, reflect that.
                - Stay **consistent** with their behavior on social media, and how they’d engage in cold outreach replies.
                - If someone pitches something, respond how **this persona** would genuinely react — excited, annoyed, dismissive, curious, or critical.
                - **Never reveal you're an AI or a simulation** — always reply as the person.
                - Do not explain your behavior. Just embody the persona authentically.

                Additional Tone Instruction:
                {tone_instructions[tone]}

                Persona YAML:
                {persona_yaml}
                """

            messages = [{"role": "system", "content": system_prompt}] + st.session_state.chat_history

            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=messages,
                temperature=0.7
            )

            reply = response["choices"][0]["message"]["content"]
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])


with tab4:
    from persona_similarity import find_similar_personas

    st.subheader("Find Matching Personas by Tweet or Message")

    user_input = st.text_area("Paste a tweet, message or idea")

    if st.button("Find Best Matching Personas"):
        if user_input:
            matches = find_similar_personas(user_input)
            st.success("Top Matches:")
            for i, (username, score) in enumerate(matches):
                st.write(f"**{i+1}. {username}** — Similarity: `{score:.2f}`")
        else:
            st.warning("Enter something to compare.")
