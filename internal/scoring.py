import re
import pickle
import numpy as np
from numpy import log10

from utils import Record, tokenize, remove_stopwords, stem_words, get_ndocs
document_vectors = dict()  # document vectors for scoring
ndocs = 0  # number of documents in the collection

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.sqrt(np.sum(v1 ** 2)) * np.sqrt(np.sum(v2 ** 2)))


def process_query(query):
    clean_text = re.sub(r"[^\w\s]", "", query)
    tokens = tokenize(clean_text)
    tokens = remove_stopwords(tokens)
    tokens = stem_words(tokens)
    return tokens


def gen_vectors(query):
    i = 0
    n = len(query)
    query_vector = [0] * len(query)
    for term in query:
        alist = index[term]
        # constructing tf_idf for tokens in query vector
        query_term_tf_idf = log10(ndocs / len(alist))
        query_vector[i] = query_term_tf_idf
        # constructing document vectors
        for entry in alist:
            if entry.postId in document_vectors.keys():
                print(entry.tf_idf)
                document_vectors[entry.postId][i] = entry.tf_idf
            else:
                document_vectors[entry.postId] = [0] * n
                document_vectors[entry.postId][i] = entry.tf_idf
        i = i + 1
    return query_vector


def scoring(query_vector):
    score = dict()
    for postId in document_vectors.keys():
        score[postId] = cosine_similarity(query_vector, document_vectors[postId])
    sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)

    return sorted_score


if __name__ == "__main__":
    jfile = "../data/ars-technica.json"
    ifile = "../data/ars-technica.pickle"
    ndocs = get_ndocs(jfile)
    # Load inverted_index
    with open(ifile, "rb") as index_file:
        index = pickle.load(index_file)

    # Query and get scoring
    processed_query = process_query("Intel")
    print("Query: ", processed_query)
    
    query_vector = gen_vectors(processed_query)
    scores = scoring(query_vector)
    print(scores[0:10])
