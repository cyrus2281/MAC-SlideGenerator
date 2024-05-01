import pyttsx3

def text_to_audio(text, output_path):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

