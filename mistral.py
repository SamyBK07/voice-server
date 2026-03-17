import requests
import json
import os

MISTRAL_API_KEY = os.getenv("PD85t8aUMKTkZGDlAWhOWyxywwYRkSq1")

MEMORY_FILE = "memory.json"

def load_memory():

    try:
        with open(MEMORY_FILE,"r") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):

    with open(MEMORY_FILE,"w") as f:
        json.dump(memory,f)

def ask_mistral(user_text, personality):

    memory = load_memory()

    messages = [{"role":"system","content":personality}]

    messages += memory

    messages.append({
        "role":"user",
        "content":user_text
    })

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization":f"Bearer {MISTRAL_API_KEY}",
            "Content-Type":"application/json"
        },
        json={
            "model":"mistral-small",
            "messages":messages
        }
    )

    data = response.json()

    reply = data["choices"][0]["message"]["content"]

    memory.append({"role":"user","content":user_text})
    memory.append({"role":"assistant","content":reply})

    memory = memory[-10:]   # limite mémoire

    save_memory(memory)

    return reply
