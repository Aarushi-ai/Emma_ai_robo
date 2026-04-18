import io
import pygame
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def play_audio(audio_bytes):
    """Plays audio from bytes using Pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(io.BytesIO(audio_bytes))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def openai_text_to_speech(text):
    """Converts text to speech and returns audio bytes."""
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=text
    )
    audio_content = response.read()
    return audio_content  # ← BUG FIX: was missing return

# Test
text = "Hi, I'm OpenAI's text to speech model"
audio = openai_text_to_speech(text)
play_audio(audio)
