import os
import pyttsx3
from openai import OpenAI
client = OpenAI()

def microsoft_text_to_audio(text, output_path):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

def openai_text_to_audio(text, output_path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
    )
    response.stream_to_file(output_path)

def text_to_audio(text, output_path):
 if os.getenv("USE_OPENAI_FOR_TEXT_TO_AUDIO"):
     return openai_text_to_audio(text, output_path)
 else:
    return microsoft_text_to_audio(text, output_path)
