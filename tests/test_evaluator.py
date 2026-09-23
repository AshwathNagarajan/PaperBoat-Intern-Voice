import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ear.recognition.evaluator import evaluate_speech


audio_path = "samples/apple.wav"
target_word = "apple"

result = evaluate_speech(audio_path, target_word)

print(result)
