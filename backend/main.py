from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os

from backend.whisper_model import transcribe_audio
from backend.summarizer import summarize_text


app = FastAPI(
    title="Voice Transcription API",
    description="Whisper based voice transcription API"
)


ALLOWED_EXTENSIONS = {".mp3", ".wav"}


@app.get("/")
def home():
    return {
        "message": "Voice Transcription API is running"
    }


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only MP3 and WAV files are supported."
        )
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temp_file:

        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:

        result = transcribe_audio(temp_path)
        transcript = result["text"].strip()
        segments = result.get("segments", [])
        if segments:
            duration = segments[-1]["end"]
        else:
            duration = 0
        key_points = summarize_text(
            transcript,
            max_points=3
        )

        return {
            "filename": file.filename,
            "duration_seconds": round(duration, 2),
            "transcription": transcript,
            "key_points": key_points
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)