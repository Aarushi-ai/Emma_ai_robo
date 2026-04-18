'''
'''









'''
Step1
Speech to text using google's speech recognition api
'''

import speech_recognition as sr
import pygame

pygame.mixer.init()

#function to play prompt audios

def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(s)


# function to convert speech to text

def listen_with_google():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        #listens
        print("Listening...")
        play_sound(".../Resources/listen.mp3")
        audio = recognizer.listen(source)
        #recognizer.adjust_for_ambient_noise(source)
        play_sound(".../Resources/convert.mp3")

        #converts
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    

    #-----------MAIN-----------
    listen_with_google()
    
