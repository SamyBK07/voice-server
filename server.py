from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import threading

from stt import transcribe
from mistral import ask_mistral
from scheduler import agent_loop

app = FastAPI()

with open("personality.txt","r",encoding="utf-8") as f:
    PERSONALITY = f.read()


@app.on_event("startup")
def start_agent():

    thread = threading.Thread(
        target=agent_loop,
        args=(PERSONALITY,),
        daemon=True
    )

    thread.start()


@app.post("/voice")
async def voice(file: UploadFile = File(...)):

    audio_path = "input.wav"

    with open(audio_path,"wb") as f:
        f.write(await file.read())

    text = transcribe(audio_path)

    reply = ask_mistral(text, PERSONALITY)

    return JSONResponse({
        "transcript": text,
        "response": reply
    })


@app.get("/")
def home():
    return {"status":"AI voice assistant running"}
