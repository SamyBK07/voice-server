from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from vosk import Model, KaldiRecognizer
import wave
import json
import requests
import os

# Initialisation serveur
app = FastAPI()

# Chargement du modèle Vosk
model = Model("model/vosk-model-small-fr-0.22")

# Chargement personnalité
with open("personality.txt","r",encoding="utf-8") as f:
    PERSONALITY = f.read()

# clé API Mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ---------------------------
# transcription audio
# ---------------------------

def transcribe(audio_path):

    wf = wave.open(audio_path,"rb")

    recognizer = KaldiRecognizer(model,wf.getframerate())

    text = ""

    while True:

        data = wf.readframes(4000)

        if len(data) == 0:
            break

        if recognizer.AcceptWaveform(data):

            result = json.loads(recognizer.Result())

            text += result.get("text"," ") + " "

    return text.strip()


# ---------------------------
# appel Mistral
# ---------------------------

def ask_mistral(user_text):

    prompt = PERSONALITY + "\nUtilisateur: " + user_text

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization":f"Bearer {MISTRAL_API_KEY}",
            "Content-Type":"application/json"
        },
        json={
            "model":"mistral-small",
            "messages":[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        }
    )

    data = response.json()

    return data["choices"][0]["message"]["content"]


# ---------------------------
# endpoint principal
# ---------------------------

@app.post("/voice")

async def voice(file: UploadFile = File(...)):

    audio_path = "input.wav"

    # sauvegarde audio
    with open(audio_path,"wb") as f:
        f.write(await file.read())

    # transcription
    text = transcribe(audio_path)

    # appel LLM
    reply = ask_mistral(text)

    return JSONResponse({
        "transcript":text,
        "response":reply
    })


# ---------------------------
# route test
# ---------------------------

@app.get("/")

def home():

    return {"status":"voice assistant server running"}
