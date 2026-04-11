from faster_whisper import WhisperModel

# Initialize Whisper model once on CPU
model = WhisperModel("base", device="cpu", compute_type="int8")

def speech_to_text(audio_path):
    segments, _ = model.transcribe(audio_path)

    text = ""
    for segment in segments:
        text += segment.text

    return text