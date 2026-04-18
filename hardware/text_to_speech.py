"""
speech_to_text.py
-----------------
Online Speech-to-Text Script for Emma AI Robot.
Uses Google's Speech Recognition API via the SpeechRecognition library.

Step 1 (Online): Speech to Text
Libraries: SpeechRecognition, pyaudio, pygame
"""

import speech_recognition as sr
import pygame

# Initialize Pygame mixer for audio feedback sounds
pygame.mixer.init()


def play_sound(file_path):
    """
    Plays a prompt/feedback audio file using Pygame.

    :param file_path: Path to the .mp3 or .wav file to play.
    """
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)  # Fixed: was tick(s) — undefined variable


def listen_with_google():
    """
    Listens via microphone and converts speech to text using Google's API.

    :return: Transcribed text string.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        play_sound("../Resources/listen.mp3")  # Fixed: was ".../Resources/..." (invalid path)

        audio = recognizer.listen(source)

        play_sound("../Resources/convert.mp3")  # Fixed: was ".../Resources/..." (invalid path)

        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text


# ----------- MAIN -----------

if __name__ == "__main__":
    while True:
        listen_with_google()
