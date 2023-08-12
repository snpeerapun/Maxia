import time
from gtts import gTTS
from io import BytesIO
import pygame

class TextToSpeech:
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
            continue