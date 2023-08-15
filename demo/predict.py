import os
import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# Load the trained model from the pickle file
with open("intent_model.pkl", "rb") as model_file:
    loaded_classifier = pickle.load(model_file)

# Load test data for prediction
with open("test_data.json", "r") as file:
    test_data = json.load(file)

# Preprocess the test data
vectorizer = CountVectorizer(vocabulary=loaded_classifier.classes_)
X_test_vec = vectorizer.transform(test_data)

# Predict intents using the loaded model
predicted_intents = loaded_classifier.predict(X_test_vec)

# Print the predicted intents
for intent in predicted_intents:
    print("Predicted Intent:", intent)
