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
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ------------ INITIALIZATIONS -------------------

# Initialize Pygame mixer
pygame.mixer.init()

# Initialize VOSK model (offline speech recognition)
model = vosk.Model("../Resources/vosk-model-en-us-0.220")
recognizer = vosk.KaldiRecognizer(model, 16000)  # Fixed: was (*args: model, 16000)

# Configure Gemini API with key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure OpenAI client with key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ----------------- Utility Functions ----------------

def play_sound(file_path):
    """
    Plays an audio file using Pygame.

    Args:
        file_path (str): The path to the audio file to be played.
    """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for audio to finish
        pygame.time.Clock().tick(5)


# --------------- Speech-to-Text Function ------------------

def listen_with_vosk():
    """
    Captures audio from the microphone and converts it to text using VOSK.

    Returns:
        str: Transcribed text from speech.
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
        if len(data) == 0:  # Skip if no audio data
            continue

        if recognizer.AcceptWaveform(data):  # Recognize speech
            play_sound("../Resources/convert.mp3")
            result = recognizer.Result()
            text = json.loads(result)["text"]
            print("You said: " + text)
            return text


# ---------------- AI Text Generation Function ------------------

def gemini_api(text):
    """
    Sends input text to the Gemini API and retrieves the generated response.

    Args:
        text (str): The input text/question for the AI.

    Returns:
        str: The AI-generated response text.
    """
    gemini_model = genai.GenerativeModel(model_name="gemini-2.5-flash-latest")
    response = gemini_model.generate_content(text)
    print("Emma says: " + response.text)
    return response.text  # Fixed: was missing return statement


# ---------------- Text-to-Speech Function ------------------

def openai_text_to_speech(text):
    """
    Converts input text to speech using OpenAI's TTS API.

    Args:
        text (str): The text to be converted to speech.

    Returns:
        bytes: The audio content in bytes format.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    audio_content = response.read()
    return audio_content


def play_audio(audio_bytes):
    """
    Plays audio from bytes using Pygame.

    Args:
        audio_bytes (bytes): The audio content in bytes format.
    """
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for audio to finish
        pygame.time.Clock().tick(10)


# ------------------- Main Loop ------------------

print("Emma AI Robo is starting...")
print("Press Ctrl+C to stop.\n")

while True:
    # Step 1: Listen and convert speech to text
    text = listen_with_vosk()

    # Step 2: Generate AI response using Gemini
    ai_response = gemini_api(text)

    # Step 3: Convert AI response text to speech
    audio_content = openai_text_to_speech(ai_response)

    # Step 4: Play the spoken response
    play_audio(audio_content)
