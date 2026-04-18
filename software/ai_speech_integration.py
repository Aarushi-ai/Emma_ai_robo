"""
ai_speech_integration.py
------------------------
Full Integration Script for Emma AI Robot.
Hardware + Software: Listen → Think → Speak + Move Servos

This is the COMPLETE Emma experience:
- VOSK offline speech-to-text
- Google Gemini AI response
- OpenAI text-to-speech
- Arduino servo control (arms + head move while Emma speaks)

Libraries: vosk, pyaudio, google-generativeai, openai, pygame, cvzone, python-dotenv
"""

import json
import io
import os
import pygame
import vosk
import pyaudio
import google.generativeai as genai
from openai import OpenAI
from cvzone.SerialModule import SerialObject
from time import sleep
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

# Arduino servo control
arduino = SerialObject(digits=3)

# Servo positions: [LServo, RServo, HServo]
last_positions = [180, 0, 90]

# ---------------------- SERVO FUNCTIONS ----------------------

def move_servo(target_positions, delay=0.0001):
    """
    Moves servos smoothly to target positions.

    :param target_positions: List of target angles [LServo, RServo, HServo]
    :param delay: Time delay between each increment step
    """
    global last_positions

    max_steps = max(abs(target_positions[i] - last_positions[i]) for i in range(3))

    if max_steps == 0:
        return

    for step in range(max_steps):
        current_positions = [
            last_positions[i] + (step + 1) * (target_positions[i] - last_positions[i]) // max_steps
            if abs(target_positions[i] - last_positions[i]) > step else last_positions[i]
            for i in range(3)
        ]
        arduino.sendData(current_positions)
        sleep(delay)

    last_positions = target_positions[:]


def speaking_gesture():
    """
    Makes Emma do a subtle head nod while speaking,
    to give a more natural talking appearance.
    """
    for _ in range(2):
        move_servo([last_positions[0], last_positions[1], 100])  # Head slightly right
        move_servo([last_positions[0], last_positions[1], 80])   # Head slightly left
    move_servo([last_positions[0], last_positions[1], 90])       # Head back to center


def listening_gesture():
    """
    Tilts Emma's head slightly to show she is listening.
    """
    move_servo([last_positions[0], last_positions[1], 110])  # Tilt head
    sleep(0.3)
    move_servo([last_positions[0], last_positions[1], 90])   # Back to center


def hello_gesture():
    """
    Makes Emma wave hello with her right arm.
    """
    move_servo([last_positions[0], 180, last_positions[2]])  # Raise right arm
    for _ in range(3):
        move_servo([last_positions[0], 150, last_positions[2]])  # Wave down
        move_servo([last_positions[0], 180, last_positions[2]])  # Wave up
    move_servo([last_positions[0], 0, last_positions[2]])    # Lower arm


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
    listening_gesture()  # Emma tilts head while listening

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
    """Plays audio from bytes via Pygame, with speaking gesture."""
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        speaking_gesture()          # Emma moves head while speaking
        pygame.time.Clock().tick(10)

# ---------------------- MAIN LOOP ----------------------

print("Emma AI Robot is ready (full hardware mode). Press Ctrl+C to stop.\n")

# Wave hello on startup
hello_gesture()

while True:
    # Step 1: Listen — Emma tilts head
    text = listen_with_vosk()

    # Step 2: Think — Gemini generates response
    ai_response = gemini_api(text)

    # Step 3: Speak — OpenAI TTS converts to audio
    audio_content = openai_text_to_speech(ai_response)

    # Step 4: Play + Move — Emma speaks and moves simultaneously
    play_audio(audio_content)
