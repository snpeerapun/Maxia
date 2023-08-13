import os
import time
import speech_recognition as sr
from gtts import gTTS
import pygame
from io import BytesIO
import tempfile
class TextToSpeech:
    @staticmethod
    def speak(text):
        mp3_file_object = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(mp3_file_object)
        pygame.mixer.pre_init(44100, 16, 2, 4096) 
        pygame.mixer.init()

        temp_filename = os.path.join(tempfile.gettempdir(), "temp_tts.mp3")
        with open(temp_filename, "wb") as temp_file:
            temp_file.write(mp3_file_object.getvalue())

        sound = pygame.mixer.Sound(temp_filename)
        sound.play()

        # Wait until the speech finishes playing
        while pygame.mixer.get_busy():
            time.sleep(0.1)  # Adjust the sleep duration as needed

        sound.stop()
        pygame.mixer.quit()

        os.remove(temp_filename)  # Clean up the temporary file


def main():
    recognizer = sr.Recognizer()

    while True:
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
