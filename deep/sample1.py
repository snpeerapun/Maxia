import random
import speech_recognition as sr
import pyttsx3

# Initialize speech recognition engine and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Response options
greeting_responses = ["Hello!", "Hi there!", "Hey!", "Greetings!"]
category_responses = {
    "weather": "The weather is nice today.",
    "time": "It's currently 2:30 PM.",
    "news": "In the latest news,...",
    "joke": "Sure, here's a joke for you: ...",
}
unknown_response = "I'm not sure what you're talking about."
acknowledgement_response = "Yes, sir."
goodbye_responses = ["Goodbye!", "Farewell!", "Take care!"]

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text) 
    engine.runAndWait()


def main():
    print("Listening...")
    consecutive_unknown_count = 0
    with sr.Microphone() as source:
        #recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio).lower()
        print("You:", recognized_text)
        consecutive_unknown_count = 0
        # Check for greetings
        if "hi jack" in recognized_text:
            response = random.choice(greeting_responses)

            # Check for specific categories
            if any(category in recognized_text for category in category_responses):
                response = acknowledgement_response+' ,you speak '+recognized_text
            # Check for exit command
            elif "exit" in recognized_text or "stop" in recognized_text:
                response = random.choice(goodbye_responses)
                print("Chat bot:", response)
                speak(response)
                #exit(0)  # Exit the program
            # Default response for unrecognized speech
            else:
                response = unknown_response

            print("Chat bot:", response)
            speak(response)

    except sr.UnknownValueError:
        consecutive_unknown_count += 1
        print("No speech detected. Count:", consecutive_unknown_count)

        if consecutive_unknown_count >= 10:  # Change the count as needed
            response = random.choice(goodbye_responses)
            print("Chat bot:", response)
            speak(response)

if __name__ == "__main__":
    while True:
        main()
