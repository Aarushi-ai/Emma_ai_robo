"""
step3:
text to speech with offline library

"""
import pyttsx3

def text_to_speech(text, voice_index=1, rate=170, volume=1.0):
    """Convert text to speech using specified voice"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')


    #Set properties
    engine.setProperty(name: 'voice', voices[voice_index].id)  # 0=male, 1=female
    engine.setProperty(name: 'rate', rate)  # speech speed
    engine.setProperty(name: 'volume', volume)  # volume(0.0 to 1.0)


    # speak the text
    engine.say(text)
    engine.runAndWait()


#-------------MAIN----------------

# Input text and voice selection
text = "hello, my name is emma, your personal ai robot!"
# call the function
text_to_speech(text)
