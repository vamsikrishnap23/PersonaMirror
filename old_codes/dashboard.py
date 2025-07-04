import streamlit as st
import os
import yaml
from wordcloud import WordCloud
import matplotlib.pyplot as plt

LEADS_DIR = "leads"

def list_usernames():
    return [name for name in os.listdir(LEADS_DIR) if os.path.isdir(os.path.join(LEADS_DIR, name))]

def load_file(username, filename):
    path = os.path.join(LEADS_DIR, username, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def load_persona_yaml(username):
    path = os.path.join(LEADS_DIR, username, "persona.yaml")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def show_wordcloud(text):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# --- Streamlit UI ---
st.set_page_config(page_title="Lead Persona Dashboard", layout="wide")
st.title("🧠 Lead Persona Dashboard")

usernames = list_usernames()

if not usernames:
    st.warning("No leads found in the 'leads/' folder.")
else:
    username = st.selectbox("Select a lead:", usernames)

    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("🔍 Tweet Preview")
        tweets = load_file(username, "tweets.txt")
        if tweets:
            for i, line in enumerate(tweets.split("\n")[:10]):
                st.markdown(f"**{i+1}.** {line.strip()}")
        else:
            st.info("No tweets found.")

        st.subheader("📨 Cold Outreach")
        outreach = load_file(username, "outreach.txt")
        if outreach:
            st.code(outreach, language="markdown")
        else:
            st.info("No outreach file.")

    with col2:
        st.subheader("👤 Persona YAML")
        persona_dict = load_persona_yaml(username)
        if persona_dict:
            st.code(yaml.dump(persona_dict, sort_keys=False), language="yaml")
        else:
            st.info("Persona file missing.")

        if tweets:
            st.subheader("☁️ Wordcloud from Tweets")
            show_wordcloud(tweets)


