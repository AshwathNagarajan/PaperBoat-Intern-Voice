# 🎙️ Voice Transcription & Summary

A lightweight web application that:

- Accepts MP3 and WAV audio files
- Converts speech to text using OpenAI Whisper
- Calculates speaking duration
- Generates 3 key points
- Allows the result to be downloaded

## Tech Stack

- Python
- FastAPI
- OpenAI Whisper
- Streamlit

## Project Structure

voice-transcriber/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── whisper_model.py
│   └── summarizer.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md

## Installation

Install dependencies:

```bash
pip install -r requirements.txt