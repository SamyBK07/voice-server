from vosk import Model, KaldiRecognizer
import wave
import json

model = Model("model/vosk-model-small-fr-0.22")

def transcribe(audio_path):

    wf = wave.open(audio_path, "rb")

    recognizer = KaldiRecognizer(model, wf.getframerate())

    text = ""

    while True:

        data = wf.readframes(4000)

        if len(data) == 0:
            break

        if recognizer.AcceptWaveform(data):

            result = json.loads(recognizer.Result())

            text += result.get("text","") + " "

    return text.strip()
