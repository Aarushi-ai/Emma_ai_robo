"""
text_to_speech_offline.py
--------------------------
Offline Text-to-Speech Script for Emma AI Robot.
Uses pyttsx3 — no internet connection required.

Step 3 (Offline Alternative): Text to Speech
Libraries: pyttsx3
"""

import pyttsx3


def text_to_speech(text, voice_index=1, rate=170, volume=1.0):
    """
    Convert text to speech using pyttsx3 (offline).

    :param text:        The string to speak aloud.
    :param voice_index: 0 = male voice, 1 = female voice
    :param rate:        Speech speed in words per minute (default 170)
    :param volume:      Volume level from 0.0 to 1.0 (default 1.0)
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Set voice, rate, and volume
    engine.setProperty('voice', voices[voice_index].id)  # Fixed: was setProperty(name: 'voice', ...)
    engine.setProperty('rate', rate)                     # Fixed: was setProperty(name: 'rate', ...)
    engine.setProperty('volume', volume)                 # Fixed: was setProperty(name: 'volume', ...)

    # Speak the text
    engine.say(text)
    engine.runAndWait()


# ------------- MAIN -------------

if __name__ == "__main__":
    text = "Hello, my name is Emma, your personal AI robot!"
    text_to_speech(text)
