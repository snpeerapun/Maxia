import os
import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
class TextRecognizer:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = None

    def load_dataset(self, dataset_path):
        training_data = []
        labels = []

        json_files = [file for file in os.listdir(dataset_path) if file.endswith('.json')]

        for json_file in json_files:
            with open(os.path.join(dataset_path, json_file), 'r') as file:
                data = json.load(file)
                training_data.extend(data)
                label = json_file.split('.')[0]
                labels.extend([label] * len(data))

        return training_data, labels

    def train_model(self, training_data, labels):
        X_train, X_test, y_train, y_test = train_test_split(training_data, labels, test_size=0.2, random_state=42)

        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.classifier = GradientBoostingClassifier()
        self.classifier.fit(X_train_vec, y_train)

    def save_model(self, model_path):
        with open(model_path, "wb") as model_file:
            pickle.dump((self.vectorizer, self.classifier), model_file)

    def load_model(self, model_path):
        with open(model_path, "rb") as model_file:
            self.vectorizer, self.classifier = pickle.load(model_file)
    def test_model(self):
        # Load the dataset
        training_data, labels = self.load_dataset('dataset')
        X_train, X_test, y_train, y_test = train_test_split(training_data, labels, test_size=0.2, random_state=42)

        X_test_vec = self.vectorizer.transform(X_test)
        predicted_intents = self.classifier.predict(X_test_vec)

        accuracy = accuracy_score(y_test, predicted_intents)
        print("Accuracy:", accuracy)

        intent_counts = {intent: list(predicted_intents).count(intent) for intent in set(predicted_intents)}

        intents = list(intent_counts.keys())
        counts = list(intent_counts.values())
        x = np.arange(len(intents))

        width = 0.35  # ความกว้างของแท่ง

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, counts, width, label='Predicted')
        rects2 = ax.bar(x + width/2, [list(y_test).count(intent) for intent in intents], width, label='Actual', alpha=0.2)

        ax.set_ylabel('Count')
        ax.set_title('Predicted vs. Actual Intent Distribution')
        ax.set_xticks(x)
        ax.set_xticklabels(intents, rotation=45)
        ax.legend()

        self.autolabel(rects1, ax)
        self.autolabel(rects2, ax)

        plt.tight_layout()
        plt.show()

    def autolabel(self, rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
            
    def predict_intent(self, text, confidence_threshold=0.7):
        if not self.vectorizer or not self.classifier:
            print("Model not loaded or trained. Use 'load_model()' or 'train_model()' to load or train a model.")
            return None, None
        
        X_test_vec = self.vectorizer.transform([text])
        predicted_proba = self.classifier.predict_proba(X_test_vec)
        max_proba = max(predicted_proba[0])
        predicted_intent = self.classifier.predict(X_test_vec)[0]
        
        if max_proba >= confidence_threshold:
            return predicted_intent, max_proba
        else:
            return "UnKnown", max_proba

# Usage

IsTrain = False

text_recognizer = TextRecognizer()

if IsTrain :
    training_data, labels = text_recognizer.load_dataset('dataset')     
    text_recognizer.train_model(training_data, labels)
    text_recognizer.test_model()
    text_recognizer.save_model('intent_model.pkl')
else :
    text_recognizer.load_model('intent_model.pkl')    
    test_data =  [
 
    {"sentence": "Turn up  volume", "intent": "volume"},
    {"sentence": "Increase volume", "intent": "volume"},
    {"sentence": "Raise volume", "intent": "volume"},
    {"sentence": "Make it louder", "intent": "volume"},
    {"sentence": "Volume up", "intent": "volume"},
    {"sentence": "Higher volume", "intent": "volume"},
    {"sentence": "Boost sound", "intent": "volume"},
    {"sentence": "Maximize volume", "intent": "volume"},
    {"sentence": "Up sound level", "intent": "volume"},
    {"sentence": "Loud sound", "intent": "volume"},
    {"sentence": "Swipe right", "intent": "swipe"},
    {"sentence": "Swipe to right", "intent": "swipe"},
    {"sentence": "Move screen right", "intent": "swipe"},
    {"sentence": "Swipe towards right", "intent": "swipe"},
    {"sentence": "Slide to right", "intent": "swipe"},
    {"sentence": "Right swipe", "intent": "swipe"},
    {"sentence": "Swipe in right direction", "intent": "swipe"},
    {"sentence": "Swipe to your right", "intent": "swipe"},
    {"sentence": "Move to right side", "intent": "swipe"},
    {"sentence": "Swipe rightwards", "intent": "swipe"},
    {"sentence": "Mute sound", "intent": "mute"},
    {"sentence": "Turn off audio", "intent": "mute"},
    {"sentence": "Silence, please", "intent": "mute"},
    {"sentence": "Please mute device", "intent": "mute"},
    {"sentence": "Set volume to zero", "intent": "mute"},
    {"sentence": "Turn sound off", "intent": "mute"},
    {"sentence": "Can you mute sound?", "intent": "mute"},
    {"sentence": "Disable audio", "intent": "mute"},
    {"sentence": "open my calendar", "intent": "calendar"},
 
 ]

    # Initialize variables for counting correct and total predictions
    correct_predictions = 0
    total_predictions = len(test_data)


    # Initialize lists to store results
    results = []

    # Iterate through test data
    for item in test_data:
        sentence = item['sentence']
        intent = item['intent']
        predicted_intent, max_proba = text_recognizer.predict_intent(sentence)
        result = "pass" if predicted_intent == intent else "fail"
        
        # Count correct predictions
        if result == "pass":
            correct_predictions += 1
        
        results.append([sentence,intent, predicted_intent,  max_proba, result])

    # Calculate accuracy
    accuracy = correct_predictions / total_predictions
    # Create a DataFrame to display the results
    result_df = pd.DataFrame(results, columns=['text',  'intent','predict', 'max_proba', 'result'])
    # Style the DataFrame to left-align the 'text' column
    styled_df = result_df.style.set_properties(**{'text-align': 'left'}, subset=['text'])

    # Print the DataFrame
    print(result_df)
    # Print summary accuracy
    print(f"Summary Accuracy: {accuracy:.2%}")
# Load and train the model
#training_data, labels = text_recognizer.load_dataset('dataset')



""" # Load the trained model
text_recognizer.load_model('intent_model.pkl')

# Sample text for prediction
sample_text = "What's on my calendar tomorow"
predicted_intent = text_recognizer.predict_intent(sample_text)
print(f"Predicted Intent for '{sample_text}': {predicted_intent}")
 """
