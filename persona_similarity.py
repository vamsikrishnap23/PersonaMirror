import os
import yaml
import numpy as np
from sentence_transformers import SentenceTransformer, util
from utils import LEADS_DIR, sanitize_yaml_file, get_persona_path

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_all_personas():
    personas = []
    for username in os.listdir(LEADS_DIR):
        user_path = os.path.join(LEADS_DIR, username)
        if os.path.isdir(user_path):
            persona_path = get_persona_path(username)
            if os.path.exists(persona_path):
                try:
                    sanitize_yaml_file(persona_path)
                    with open(persona_path, "r", encoding="utf-8") as f:
                        persona_yaml = yaml.safe_load(f)
                        full_text = yaml.dump(persona_yaml)
                        personas.append((username, full_text))
                except:
                    pass  
    return personas

def find_similar_personas(input_text, top_k=3):
    input_embedding = model.encode(input_text, convert_to_tensor=True)
    persona_data = load_all_personas()

    results = []
    for username, persona_text in persona_data:
        persona_embedding = model.encode(persona_text, convert_to_tensor=True)
        similarity = util.cos_sim(input_embedding, persona_embedding).item()
        results.append((username, similarity))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]
