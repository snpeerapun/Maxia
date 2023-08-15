import random
import speech_recognition as sr
import pyttsx3

# Initialize speech recognition engine and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Response options for greetings
greeting_responses = ["Hello!", "Hi there!", "Hey!", "Greetings!"]

# Response options for different categories
category_responses = {
    "weather": "The weather is nice today.",
    "time": "It's currently 2:30 PM.",
    "news": "In the latest news,...",
    "joke": "Sure, here's a joke for you: ...",
}

# Response for unknown category
unknown_response = "I'm not sure what you're talking about."

# Response for acknowledging the command
acknowledgement_response = "Yes, sir."

# Response options for goodbye
goodbye_responses = ["Goodbye!", "Farewell!", "Take care!"]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print("Listening...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        recognized_text = recognizer.recognize_google(audio).lower()
        print("You:", recognized_text)

        if "hi maxi" in recognized_text:
            response = random.choice(greeting_responses)
        else:
            detected_category = None
            for category in category_responses:
                if category in recognized_text:
                    detected_category = category
                    break

            if detected_category:
                response = acknowledgement_response
            else:
                response = unknown_response

        print("Chat bot:", response)
        speak(response)

    except sr.UnknownValueError:
        print("No speech detected.")
        response = random.choice(goodbye_responses)
        print("Chat bot:", response)
        speak(response)

if __name__ == "__main__":
    while True:
        main()
