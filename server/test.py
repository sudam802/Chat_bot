import random
import json
import pickle
import numpy as np

import nltk
#WordNetLemmatizer reduce the word to stem so that it wont loose performance
nltk.download('punkt_tab')
from nltk.stem import WordNetLemmatizer
sentence = "Hello, world! How are you doing today?"

words=nltk.word_tokenize(sentence)
print(words)