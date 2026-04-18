"""
ai_speech_integration.py
-------------------------
AI + Speech Integration Bridge for Emma AI Robot.

This module ties together the speech-to-text input,
AI language model processing, and text-to-speech output
into a single pipeline — the core "listen → think → speak" loop of Emma.

Flow:
    Microphone → speech_to_text → ai_model → text_to_speech → Speaker

Libraries: See individual modules
"""
import json
import io
import pygame
import vosk
import pyaudio
import google.generativeai as genai
from openai import OpenAI
import os

# ------------ INITIALIZATIONS -------------------

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize VOSK model
model = vosk.Model("../Resources/vosk-model-en-us-0.220")
recognizer = vosk.KaldiRecognizer(model, 16000)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------- Utility functions ----------------

def play_sound(file_path):
    """Plays an audio file using Pygame."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# --------------- Speech-to-text function ------------------

def listen_with_vosk():
    """Captures audio from the microphone and converts it to text using VOSK."""
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
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

# ---------------- AI text generation function ------------------

def gemini_api(text):
    """Sends input text to the Gemini API and retrieves the generated response."""
    gemini_model = genai.GenerativeModel(model_name="gemini-2.5-flash-latest")
    response = gemini_model.generate_content(text)
    print(response.text)
    return response.text  # ← BUG FIX: was missing return

# ---------------- Text-to-speech function ------------------

def openai_text_to_speech(text):
    """Converts input text to speech using OpenAI's TTS API."""
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    audio_content = response.read()
    return audio_content

def play_audio(audio_bytes):
    """Plays audio from bytes using Pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ------------------- Main loop ------------------

while True:
    text = listen_with_vosk()
    ai_response = gemini_api(text)
    audio_content = openai_text_to_speech(ai_response)
    play_audio(audio_content)
