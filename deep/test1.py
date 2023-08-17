import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import matplotlib.pyplot as plt

sample_data = [
    ["Turn up the volume", "volume"],
    ["Increase the volume", "volume"],
    ["Raise the volume", "volume"],
    ["Make it louder", "volume"],
    ["Volume up", "volume"],
    ["Higher volume", "volume"],
    ["Boost the sound", "volume"],
    ["Maximize the volume", "volume"],
    ["Up the sound level", "volume"],
    ["Loud sound", "volume"],
    ["Swipe right", "swipe"],
    ["Swipe to the right", "swipe"],
    ["Move right", "swipe"],
    ["Swipe towards the right", "swipe"],
    ["Slide to the right", "swipe"],
    ["Right swipe", "swipe"],
    ["Swipe in the right direction", "swipe"],
    ["Swipe to your right", "swipe"],
    ["Move to the right side", "swipe"],
    ["Swipe rightwards", "swipe"],
    ["Mute the sound", "mute"],
    ["Turn off the audio", "mute"],
    ["Silence, please", "mute"],
    ["Please mute the device", "mute"],
    ["Set the volume to zero", "mute"],
    ["Turn the sound off", "mute"],
    ["Can you mute the sound?", "mute"],
    ["Disable audio", "mute"],
    # Continue adding more data here...
]


# Separate data into input (X) and output (y)
X = [data[0] for data in sample_data]
y = [data[1] for data in sample_data]

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
vocab_size = len(tokenizer.word_index) + 1

# Convert text data to sequences of integers
X_sequences = tokenizer.texts_to_sequences(X)

# Padding sequences
max_sequence_length = max([len(seq) for seq in X_sequences])
X_padded = pad_sequences(X_sequences, maxlen=max_sequence_length, padding='post')

# Convert output labels to categorical
unique_labels = list(set(y))
label_to_index = {label: index for index, label in enumerate(unique_labels)}
y_encoded = [label_to_index[label] for label in y]

# Build the model
model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=128, input_length=max_sequence_length))
model.add(LSTM(128))
model.add(Dense(len(unique_labels), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_padded, np.array(y_encoded), epochs=50, batch_size=16, validation_split=0.2)

# Test sentences
test_sentences = [
    "Turn up the volume",
    "Swipe right",
    "Swipe in the right"
]

# Calculate accuracy for each test sentence
accuracies = []
for test_sentence in test_sentences:
    test_sequence = tokenizer.texts_to_sequences([test_sentence])
    test_padded = pad_sequences(test_sequence, maxlen=max_sequence_length, padding='post')
    predicted_index = np.argmax(model.predict(test_padded), axis=-1)
    predicted_label = unique_labels[predicted_index[0]]
    true_label = test_sentence.split()[-1]  # Assuming the last word is the true label
    accuracy = 1 if predicted_label == true_label else 0
    accuracies.append(accuracy)

# Calculate average accuracy
average_accuracy = sum(accuracies) / len(accuracies)
print(f"Average accuracy: {average_accuracy:.2f}")
