import json
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load data from JSON file
with open('D:\project\Maxia\demo\data.json', 'r') as json_file:
    data = json.load(json_file)

texts = [entry['text'] for entry in data['data']]
labels = [entry['label'] for entry in data['data']]

# Tokenize and pad the sequences
tokenizer = Tokenizer(oov_token='<OOV>')
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, padding='post', truncating='post')

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

# Build a simple LSTM model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64),
    LSTM(64),
    Dense(len(set(labels)), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Save the trained model
model.save('speech_recognition_model.h5')

# Test and predict using the trained model
sample_texts = ["What's the weather like?", "Play a song for me", "Remind me to buy groceries"]
sample_sequences = tokenizer.texts_to_sequences(sample_texts)
sample_padded_sequences = pad_sequences(sample_sequences, padding='post', truncating='post')

predictions = model.predict(sample_padded_sequences)

for i, text in enumerate(sample_texts):
    predicted_label = labels[predictions[i].argmax()]
    print(f"Text: {text} | Predicted Label: {predicted_label}")
