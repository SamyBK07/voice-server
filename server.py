from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
import os

from stt import transcribe
from mistral import ask_mistral
from tts import generate_tts

app = FastAPI()

with open("personality.txt","r",encoding="utf-8") as f:
    PERSONALITY = f.read()

@app.post("/voice")
async def voice(file: UploadFile = File(...)):

    audio_path = "input.wav"

    with open(audio_path,"wb") as f:
        f.write(await file.read())

    # STT
    text = transcribe(audio_path)

    # LLM
    reply = ask_mistral(text, PERSONALITY)

    # TTS
    audio_reply = generate_tts(reply)

    return FileResponse(
        audio_reply,
        media_type="audio/wav"
    )


@app.get("/")
def home():
    return {"status":"AI voice server running"}
