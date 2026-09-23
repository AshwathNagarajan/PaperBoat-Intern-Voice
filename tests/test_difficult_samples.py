import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ear.recognition.evaluator import evaluate_speech


SAMPLES = [
    "samples/apple.wav",
    "samples/apple_appl_clean.wav",
    "samples/apple_appu_clean.wav",
    "samples/apple_fast_pitch.wav",
    "samples/apple_noisy.wav",
    "samples/apple_muffled_quiet.wav",
    "samples/apple_heavy_noise.wav",
    "samples/apple_slow_muffled.wav",
]


for audio_path in SAMPLES:
    result = evaluate_speech(audio_path, "apple")
    print(Path(audio_path).name, result)
