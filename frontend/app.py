import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/transcribe"


st.set_page_config(
    page_title="Voice Transcription",
    page_icon="🎙️",
    layout="centered"
)


st.title("🎙️ Voice Transcription")
st.write(
    "Upload a short MP3 or WAV recording "
    "to transcribe speech and generate key points."
)


audio_file = st.file_uploader(
    "Upload your voice recording",
    type=["mp3", "wav"]
)


if audio_file:

    st.audio(
        audio_file,
        format=audio_file.type
    )

    st.write(
        f"**File:** {audio_file.name}"
    )


    if st.button(
        "🚀 Transcribe",
        use_container_width=True
    ):

        with st.spinner(
            "Processing audio with Whisper..."
        ):

            try:

                files = {
                    "file": (
                        audio_file.name,
                        audio_file.getvalue(),
                        audio_file.type
                    )
                }

                response = requests.post(
                    API_URL,
                    files=files
                )

                if response.status_code == 200:

                    data = response.json()
                    st.session_state["result"] = data

                else:

                    st.error(
                        f"Error: {response.json().get('detail', 'Unknown error')}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend. "
                    "Make sure the backend is running."
                )


if "result" in st.session_state:

    data = st.session_state["result"]

    st.divider()

    st.subheader("⏱️ Speaking Duration")

    duration = data["duration_seconds"]

    if duration < 60:
        duration_text = f"{duration:.1f} seconds"
    else:
        minutes = int(duration // 60)
        seconds = int(duration % 60)

        duration_text = (
            f"{minutes} min {seconds} sec"
        )

    st.metric(
        "Duration",
        duration_text
    )


    st.subheader("📝 Transcription")

    transcript = data["transcription"]

    st.text_area(
        "Transcript",
        transcript,
        height=200,
        label_visibility="collapsed"
    )


    st.subheader("✨ Key Points")

    key_points = data["key_points"]

    if key_points:

        for point in key_points:
            st.markdown(
                f"• {point}"
            )

    else:

        st.info(
            "Not enough content to generate key points."
        )


    download_text = (
        f"TRANSCRIPTION\n"
        f"====================\n\n"
        f"{transcript}\n\n"
        f"SPEAKING DURATION\n"
        f"====================\n\n"
        f"{duration_text}\n\n"
        f"KEY POINTS\n"
        f"====================\n\n"
    )

    for point in key_points:
        download_text += f"• {point}\n"

    st.download_button(
        label="⬇️ Download Result",
        data=download_text,
        file_name="transcription.txt",
        mime="text/plain",
        use_container_width=True
    )