"""
main.py
-------
Main Pipeline Script for Emma AI Robot.
Software-only: Listen → Think → Speak
No hardware/servo control — use this to test AI and voice without Arduino.

Libraries: vosk, pyaudio, google-generativeai, openai, pygame, python-dotenv
"""

import json
import io
import os
import pygame
import vosk
import pyaudio
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

# ---------------------- LOAD ENV VARIABLES ----------------------

load_dotenv()

# ---------------------- INITIALIZATIONS ----------------------

pygame.mixer.init()

# VOSK offline speech recognition
model = vosk.Model("../Resources/vosk-model-en-us-0.22")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# OpenAI TTS
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------- UTILITY ----------------------

def play_sound(file_path):
    """Plays a short feedback audio file via Pygame."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# ---------------------- SPEECH TO TEXT ----------------------

def listen_with_vosk():
    """
    Captures microphone audio and converts to text using VOSK (offline).
    Returns: Transcribed text string.
    """
    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )
    stream.start_stream()
    print("Listening...")
    play_sound("../Resources/listen.mp3")

    while True:
        data = stream.read(8192)
        if len(data) == 0:
            continue
        if recognizer.AcceptWaveform(data):
            play_sound("../Resources/convert.mp3")
            result = recognizer.Result()
            text = json.loads(result)["text"]
            print("You said: " + text)
            return text

# ---------------------- AI RESPONSE ----------------------

def gemini_api(text):
    """
    Sends text to Gemini and returns the AI response.
    Returns: AI-generated response string.
    """
    gemini_model = genai.GenerativeModel(model_name="gemini-2.5-flash-latest")
    response = gemini_model.generate_content(text)
    print("Emma says: " + response.text)
    return response.text

# ---------------------- TEXT TO SPEECH ----------------------

def openai_text_to_speech(text):
    """
    Converts text to speech using OpenAI TTS.
    Returns: Audio content as bytes.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    return response.read()


def play_audio(audio_bytes):
    """Plays audio from bytes via Pygame."""
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ---------------------- MAIN LOOP ----------------------

print("Emma AI is ready (software mode). Press Ctrl+C to stop.\n")

while True:
    # Step 1: Listen
    text = listen_with_vosk()

    # Step 2: Think
    ai_response = gemini_api(text)

    # Step 3: Speak
    audio_content = openai_text_to_speech(ai_response)

    # Step 4: Play
    play_audio(audio_content)
