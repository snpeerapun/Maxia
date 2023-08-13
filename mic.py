import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# List available microphones
available_microphones = sr.Microphone.list_microphone_names()

print("Available Microphones:")
for idx, mic in enumerate(available_microphones):
    print(f"{idx + 1}. {mic}")

# Select a microphone (you can change the index)
selected_microphone_index = int(input("Select a microphone (enter index): ")) - 1

# Capture audio from the selected microphone
with sr.Microphone(device_index=selected_microphone_index) as source:
    print(f"Using microphone: {available_microphones[selected_microphone_index]}")
    print("Say something...")
    audio = recognizer.listen(source)

# Recognize speech using Google Web Speech API
try:
    recognized_text = recognizer.recognize_google(audio)
    print(f"You said: {recognized_text}")
except sr.UnknownValueError:
    print("Sorry, could not understand audio.")
except sr.RequestError as e:
    print(f"Error connecting to the Google Web Speech API: {e}")
