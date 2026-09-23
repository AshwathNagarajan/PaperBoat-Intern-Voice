from __future__ import annotations

import os
import re
from functools import lru_cache

import whisper
from jiwer import cer, wer
from rapidfuzz.distance import Levenshtein


WHISPER_MODEL = "tiny.en"
NEAR_MATCH_THRESHOLD = 60.0


@lru_cache(maxsize=1)
def _load_model():
    return whisper.load_model(WHISPER_MODEL)


def _normalize_text(text: str) -> str:
    text = text.lower().strip() if text else ""
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def evaluate_speech(audio_path: str, target_word: str) -> dict:
    if not isinstance(audio_path, str):
        raise TypeError("audio_path must be a string")

    if not isinstance(target_word, str):
        raise TypeError("target_word must be a string")

    target = _normalize_text(target_word)

    if not target:
        raise ValueError("target_word cannot be empty")

    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file does not exist: {audio_path}")

    audio = whisper.load_audio(audio_path)
    result = _load_model().transcribe(
        audio,
        language="en",
        task="transcribe",
        temperature=0,
        fp16=False,
    )

    spoken = _normalize_text(result.get("text", ""))

    if not spoken:
        return {
            "spoken_transcript": "",
            "target_word": target,
            "accuracy_score": 0.0,
            "status": "MISMATCH",
        }

    levenshtein_score = Levenshtein.normalized_similarity(spoken, target) * 100
    cer_score = max(0.0, 1.0 - cer(target, spoken)) * 100
    wer(target, spoken)

    accuracy_score = round(
        max(0.0, min(100.0, (levenshtein_score + cer_score) / 2)),
        2,
    )

    if spoken == target:
        status = "EXACT"
    elif accuracy_score >= NEAR_MATCH_THRESHOLD:
        status = "NEAR_MATCH"
    else:
        status = "MISMATCH"

    return {
        "spoken_transcript": spoken,
        "target_word": target,
        "accuracy_score": accuracy_score,
        "status": status,
    }
