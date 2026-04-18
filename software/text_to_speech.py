"""
text_to_speech.py
-----------------
Online Text-to-Speech Script for Emma AI Robot.
Uses OpenAI's TTS API for high-quality voice output.

Libraries: openai, pygame, python-dotenv
"""

import io
import os
import pygame
from openai import OpenAI  # Fixed: was "from openai import" (incomplete import)
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def play_audio(audio_bytes):
    """
    Plays audio from bytes using Pygame.

    :param audio_bytes: Audio content in bytes format.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def openai_text_to_speech(text):
    """
    Converts text to speech using OpenAI TTS API.

    :param text: Input text string to speak.
    :return:     Audio content as bytes.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text
    )
    return response.read()  # Fixed: was missing return statement


# ----------- MAIN -----------

if __name__ == "__main__":
    text = "Hello, I'm Emma, your personal AI robot!"
    audio = openai_text_to_speech(text)
    play_audio(audio)
