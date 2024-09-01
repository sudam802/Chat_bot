from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

@app.route('/predict', methods=['POST'])
def predict():
    try:
        message = request.json['message']
        print('message came')
        intents = predict_class(message, model)
        return jsonify({'intents': intents})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'})

if __name__ == '__main__':
    app.run(port=5000)
