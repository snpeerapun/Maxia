import pickle
from sklearn.feature_extraction.text import CountVectorizer

class TextRegconize:
    def __init__(self):
        self.pipeline = None
   
    
    def load_model(self,model_filename='intent_model.pkl'):
        with open(model_filename, "rb") as model_file:
            vectorizer, classifier = pickle.load(model_file)
        return vectorizer, classifier
    
    def predict_intent(self, text):
        preprocessed_text = self.preprocess_text(text)
        predicted_intent = self.model.predict(preprocessed_text)
        return predicted_intent[0]

# Load the trained vectorizer and classifier model
 
# Usage

text_recognizer = TextRegconize()
# Load the trained model
loaded_vectorizer, loaded_classifier = text_recognizer.load_model('intent_model.pkl')

 
# Sample text for prediction
sample_text = "Turn up the volume"
predicted_intent = text_recognizer.predict_intent(loaded_vectorizer, loaded_classifier, sample_text)

print(f"Predicted Intent for '{sample_text}': {predicted_intent}")
