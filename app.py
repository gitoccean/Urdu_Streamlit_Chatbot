import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import openai

openai.api_key = ''

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Say something in Urdu!")
        audio = r.listen(source)
        st.write("Recording complete!")
    return audio

def transcribe_audio(audio):
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio, language='ur')
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def text_to_speech(text, lang='ur'):
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")
    return "response.mp3"

def play_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    play(audio)

def main():
    st.title("Urdu Voice Assistant")

    if st.button("Record Voice"):
        audio = record_audio()
        text = transcribe_audio(audio)
        st.write("Transcribed Text:", text)

        if text:
            response = generate_response(text)
            st.write("Response:", response)

            audio_file = text_to_speech(response)
            st.audio(audio_file)
            play_audio(audio_file)

if __name__ == "__main__":
    main()
