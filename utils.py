import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_DIR = os.path.join(BASE_DIR, "leads")

def get_user_dir(username):
    return os.path.join(LEADS_DIR, username)

def get_tweets_path(username):
    return os.path.join(get_user_dir(username), "tweets.txt")

def get_persona_path(username):
    return os.path.join(get_user_dir(username), "persona.yaml")

def get_outreach_path(username):
    return os.path.join(get_user_dir(username), "cold_outreach.txt")

def sanitize_yaml_file(filepath):
    """Clean yaml file by removing backtick blocks like ```yaml ... ```"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        if not line.strip().startswith("```"):
            cleaned_lines.append(line)

    # Rewrite cleaned YAML
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)



