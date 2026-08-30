import whisper

# Lightweight model
model = whisper.load_model("base")


def transcribe_audio(audio_path):
    result = model.transcribe(
        audio_path,
        fp16=False
    )

    return result