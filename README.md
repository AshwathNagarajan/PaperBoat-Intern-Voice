# 🎙️ Voice Transcription & Summary

A lightweight web application for transcribing short voice recordings using **OpenAI Whisper** and generating a **3-bullet key-point summary** with speaking duration.

## ✨ Features

- 🎵 MP3 / WAV upload
- 🎙️ Whisper speech-to-text
- ⏱️ Speaking duration
- ✨ 3 key-point summary
- 📥 Download results
- ⚡ Lightweight and laptop-friendly

## 🛠️ Tech Stack

- Python
- FastAPI
- OpenAI Whisper
- Streamlit
- PyTorch

## 📁 Project Structure

```text
voice-transcriber/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── whisper_model.py
│   └── summarizer.py
├── frontend/
│   └── app.py
├── .gitignore
├── requirements.txt
└── README.md