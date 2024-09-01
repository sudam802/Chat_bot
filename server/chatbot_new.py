from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import pickle
import numpy as np


import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model
# creating the app
app = Flask(__name__)
CORS(app)

# Initialize the lemmatizer and load the necessary files
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents_2.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model_ad.h5')  # The output will be numerical data

# Clean up the sentence by tokenizing and lemmatizing it
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Convert the sentence into a bag of words representation
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predict the class of the sentence
def predict_class(sentence):
    bow = bag_of_words(sentence)  # bow: Bag Of Words, feed the data into the neural network
    res = model.predict(np.array([bow]))[0]  # res: result. [0] as index 0
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Main loop to get user input and output predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        message = request.json.get('message')
        print(message)
        intents_list = predict_class(message)
        for intent in intents['intents']:
            if intent['tag'] == intents_list[0]['intent']:
                response = random.choice(intent['responses'])
                print(response)
                return jsonify({'intents': {'intent': response}})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'})
    
if __name__ == '__main__':
    app.run(port=5000)



