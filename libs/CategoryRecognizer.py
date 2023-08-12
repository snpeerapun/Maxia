import spacy
from sklearn.metrics.pairwise import cosine_similarity
import os
import json

class CategoryRecognizer:
    def __init__(self,):
        self.folder_path = "dataset"
        self.dataset = {}
        self.load_dataset()

    def load_dataset(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                category = os.path.splitext(filename)[0]
                file_path = os.path.join(self.folder_path, filename)

                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                    if category not in self.dataset:
                        self.dataset[category] = []

                    self.dataset[category].extend(data)

    def get_most_similar_category(self, target_sentence):
        max_similarity = -1
        best_category = None

        nlp = spacy.load("en_core_web_sm")

        def get_sentence_embedding(sentence):
            doc = nlp(sentence)
            vectors = [token.vector for token in doc]
            return sum(vectors) / len(vectors)

        def compare_sentences(sentence1, sentence2):
            emb1 = get_sentence_embedding(sentence1)
            emb2 = get_sentence_embedding(sentence2)
            similarity = cosine_similarity([emb1], [emb2])[0][0]
            return similarity

        for category, sentences in self.dataset.items():
            for sentence in sentences:
                similarity_score = compare_sentences(target_sentence, sentence)
                if similarity_score > max_similarity:
                    max_similarity = similarity_score
                    best_category = category

        return best_category