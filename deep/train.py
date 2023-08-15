import os
import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Initialize lists to store training data and labels
training_data = []
labels = []

# Load training data from all JSON files in the 'dataset' directory
json_files = [file for file in os.listdir('dataset') if file.endswith('.json')]

for json_file in json_files:
    with open(os.path.join('dataset', json_file), 'r') as file:
        data = json.load(file)
        training_data.extend(data)
        label = json_file.split('.')[0]  # Use the filename as the label
        labels.extend([label] * len(data))

# Split the data into training and testing sets (80:20 split)
X_train, X_test, y_train, y_test = train_test_split(training_data, labels, test_size=0.2, random_state=42)

# Preprocess the training data (tokenization, feature extraction, etc.)
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

# Train a classifier (Naive Bayes in this example)
classifier = MultinomialNB()
classifier.fit(X_train_vec, y_train)

# Save the trained model as a pickle file
with open("intent_model.pkl", "wb") as model_file:
    pickle.dump(classifier, model_file)

# Load the trained model from the pickle file
with open("intent_model.pkl", "rb") as model_file:
    loaded_classifier = pickle.load(model_file)

# Preprocess the test data
X_test_vec = vectorizer.transform(X_test)

# Predict intents using the loaded model
predicted_intents = loaded_classifier.predict(X_test_vec)

# Calculate accuracy
accuracy = accuracy_score(y_test, predicted_intents)
print("Accuracy:", accuracy)

# Print test data, true intent, and predictions
 
# Print formatted table with test data, true intent, and predicted intent
print("| Test Data                                 | True Intent | Predicted Intent | Result   |")
print("|------------------------------------------ |-------------|------------------|----------|")
for i in range(len(X_test)):
    result = "Pass" if y_test[i] == predicted_intents[i] else "Fail"
    print(f"| {X_test[i]:<40} | {y_test[i]:<11} | {predicted_intents[i]:<16} | {result:<8} |")


# Count the occurrences of each intent in predicted intents
predicted_intent_counts = {intent: list(predicted_intents).count(intent) for intent in set(predicted_intents)}

# Create a bar chart for predicted intent distribution
predicted_intents = list(predicted_intent_counts.keys())
predicted_counts = list(predicted_intent_counts.values())
x = np.arange(len(predicted_intents))

plt.bar(x, predicted_counts, align="center")
plt.xticks(x, predicted_intents, rotation=45)
plt.xlabel("Predicted Intents")
plt.ylabel("Count")
plt.title("Predicted Intent Distribution")
plt.tight_layout()
plt.show()

 