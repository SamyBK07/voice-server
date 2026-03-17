from TTS.api import TTS

tts = TTS(model_name="tts_models/fr/css10/vits")

def generate_tts(text):

    output = "response.wav"

    tts.tts_to_file(
        text=text,
        file_path=output
    )

    return output
