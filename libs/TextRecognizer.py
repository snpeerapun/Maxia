 
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
import os
import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

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
        X_train, X_test, y_train, y_test = train_test_split(training_data, labels, test_size=0.5, random_state=42)

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
        rects2 = ax.bar(x + width/2, [list(y_test).count(intent) for intent in intents], width, label='Actual', alpha=0.5)

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
            
    def predict_intent(self, text):
        if not self.vectorizer or not self.classifier:
            print("Model not loaded or trained. Use 'load_model()' or 'train_model()' to load or train a model.")
            return

        X_test_vec = self.vectorizer.transform([text])
        predicted_intent = self.classifier.predict(X_test_vec)
        return predicted_intent[0]
