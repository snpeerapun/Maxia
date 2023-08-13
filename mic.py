import speech_recognition as sr
from io import BytesIO
from gtts import gTTS
import tempfile
import os
import time
import pygame.mixer

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

# Initialize the recognizer
recognizer = sr.Recognizer()

def display_microphone_list():
    print("Available Microphone Devices:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")
    print()

def main():
    display_microphone_list()

    try:
      
        
        with sr.Microphone() as source:
            print("Listening for speech...")

            while True:
                try:
                    audio = recognizer.listen(source, timeout=5)  # Capture audio for up to 5 seconds

                    if audio is None:
                        print("No audio captured. Make sure the microphone is working properly.")
                        continue  # Skip processing if no audio is captured

                    recognized_text = recognizer.recognize_google(audio)
                    print("You said:",recognized_text)
                    TextToSpeech.speak("You said:"+recognized_text)
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand what you said.")
                except sr.RequestError as e:
                    print("Sorry, I encountered an error during speech recognition:", str(e))

                print("Listening again...")

    except ValueError:
        print("Invalid input. Please enter a valid microphone index.")
    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == "__main__":
    main()
