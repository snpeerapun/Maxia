import time
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import pygame

class TextToSpeech:
    @classmethod
    def speak(cls, text):
        mp3_file_object = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(mp3_file_object)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file_object)
        pygame.mixer.music.play()

        # Wait until the speech finishes playing
        while pygame.mixer.music.get_busy():
            continue

def main():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        print(f"You said: {recognized_text}")
        
        response_text = f"You said: {recognized_text}"
        TextToSpeech.speak(response_text)
        
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Error connecting to the Google Web Speech API: {e}")

if __name__ == "__main__":
    main()