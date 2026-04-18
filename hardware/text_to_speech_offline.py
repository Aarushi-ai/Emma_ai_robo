"""
speech_to_text_offline.py
--------------------------
Offline Speech-to-Text Script for Emma AI Robot.
Uses the VOSK library — no internet connection required.

Step 1 (Offline Alternative): Speech to Text
Download VOSK model from: https://alphacephei.com/vosk/models  (Fixed: was alphacephei.om)

Libraries: vosk, pyaudio, pygame
"""

import vosk
import pyaudio
import json
import pygame

# Initialize Pygame mixer for audio feedback
pygame.mixer.init()

# Load the VOSK offline model
model = vosk.Model("../Resources/vosk-model-en-us-0.22")
recognizer = vosk.KaldiRecognizer(model, 16000)  # Fixed: was KaldiRecognizer(*args:model, 16000)


def play_sound(file_path):
    """
    Plays a prompt/feedback audio file using Pygame.

    :param file_path: Path to the .mp3 or .wav file to play.
    """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)


def listen_with_vosk():
    """
    Listens via microphone and converts speech to text using VOSK (offline).

    :return: Transcribed text string.
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
    play_sound("../Resources/listen.mp3")  # Fixed: was ".../Resources/..." (invalid path)

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


# ------------ MAIN ----------------

if __name__ == "__main__":
    while True:
        listen_with_vosk()
