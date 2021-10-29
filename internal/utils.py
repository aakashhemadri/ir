import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
import json

class Record:
    def __init__(self, uuid, postId, frequency, tf_idf=0):
        self.uuid = uuid
        self.postId = postId
        self.frequency = frequency
        self.tf_idf = tf_idf

    def __repr__(self):
        return str(self.__dict__)


def tokenize(document):
    tokens = nltk.word_tokenize(document, language="english")
    return tokens


def remove_stopwords(tokens):
    processed_tokens = []
    for token in tokens:
        token = token.lower()
        if token not in stop_words:
            processed_tokens.append(token)
    return processed_tokens


def stem_words(tokens):
    ps = PorterStemmer()
    lemmatized_tokens = []
    for token in tokens:
        lemmatized_tokens.append(ps.stem(token))
    return lemmatized_tokens

def get_ndocs(file_path):
    with open(file_path, "r") as file:
        documents = json.load(file)
    
    return len(documents)
