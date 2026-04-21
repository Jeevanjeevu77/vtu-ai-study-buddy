import os
from groq import Groq

def speech_to_text(audio_path):
    """Transcribes audio using Groq's Cloud Whisper API (whisper-large-v3)."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
          file=(audio_path, file.read()),
          model="whisper-large-v3",
          response_format="text"
        )
    return transcription