import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
# nltk.download('punkt')
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

doc=[]
for intent in intents['intents']:
    for pattern in intent['patterns']:
        words=nltk.tokenize.word_tokenize(pattern)
        doc.append((words,intent['tag']))
print(doc)


