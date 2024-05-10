import json
import numpy as np
import pickle
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D

from flask import Flask, render_template, request, jsonify

app=Flask(__name__)

with open('intents.json', 'r') as file:
    intents = json.load(file)

patterns = []
tags = []
responses = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])
    responses.extend(intent['responses'])

print("patterns",patterns)
print("tags",tags)
print("responses",responses)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(patterns)
print(tokenizer)

word_index = tokenizer.word_index
vocab_size = len(word_index) + 1
print(word_index)
#exit()
sequences = tokenizer.texts_to_sequences(patterns)
max_sequence_length = max([len(seq) for seq in sequences])
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')
print(padded_sequences)

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(tags)
num_classes = len(set(encoded_labels))
print("labels",encoded_labels)
model = Sequential([
    Embedding(vocab_size, 64, input_length=max_sequence_length),
    GlobalAveragePooling1D(),
    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(padded_sequences, np.array(encoded_labels), epochs=100, verbose=1)

model.summary()

def preprocess_input(text):
    sequence = tokenizer.texts_to_sequences([text])
    print(sequence)
    padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length, padding='post')
    print(padded_sequence)
    return padded_sequence

def get_intent(text):
    preprocessed_text = preprocess_input(text)
    prediction = model.predict(preprocessed_text)
    predicted_tag = label_encoder.inverse_transform([np.argmax(prediction)])
    print(predicted_tag)
    return predicted_tag[0]

def get_response(intent):
    for intent_item in intents['intents']:
        if intent_item['tag'] == intent:
            return np.random.choice(intent_item['responses'])
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_input=request.json['message']
    intent=get_intent(user_input)
    response=get_response(intent)
    return jsonify({'message':response})

if __name__ == '__main__':
    app.run(debug=True)
    
# print("Bot: Hello! How can I assist you?")

# while True:
#     user_input = input("User: ")
#     if user_input.lower() == 'quit':
#         print("Bot: Goodbye!")
#         break
#     else:
#         intent = get_intent(user_input)
#         response = get_response(intent)
#         print("Bot:", response)
