import os
import time
from gtts import gTTS
from io import BytesIO
import pygame
import tempfile
import pyttsx3

class TextToSpeech:
    @staticmethod
    def speak(text):
        wav_file_object = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(wav_file_object)

        pygame.mixer.init()

        temp_filename = os.path.join(tempfile.gettempdir(), "temp_tts.mp3")
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(wav_file_object.getvalue())

        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        # Wait until the speech finishes playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)  # Adjust the sleep duration as needed

        pygame.mixer.music.stop()
        pygame.mixer.quit()

        os.remove(temp_filename)  # Clean up the temporary file

    def speak2(audio):
        
        engine = pyttsx3.init()
        # getter method(gets the current value
        # of engine property)
        voices = engine.getProperty('voices')
        
        # setter method .[0]=male voice and
        # [1]=female voice in set Property.
        engine.setProperty('voice', voices[0].id)
        
        # Method for the speaking of the assistant
        engine.say(audio) 
        
        # Blocks while processing all the currently
        # queued commands
        engine.runAndWait()

""" class TextToSpeech:
    @classmethod
    def speak(cls, text):
        
        mp3_file_object = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(mp3_file_object)

        # Rewind the BytesIO object to the beginning to play it from the start
        mp3_file_object.seek(0)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file_object)
        pygame.mixer.music.play()
        
        # Wait until the speech finishes playing
        while pygame.mixer.music.get_busy():
            continue """