import whisper
import os

# Add Homebrew path for macOS if needed
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"

model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]
