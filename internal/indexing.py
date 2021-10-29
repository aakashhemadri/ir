import json
import pickle
import datetime
import uuid
from numpy import log10
import numpy as np
from utils import Record, tokenize, remove_stopwords, stem_words

index_dict = dict()  # inverted_index
ndocs = 0

def iindex(document):
    tokens = tokenize(document["content"])
    tokens = remove_stopwords(tokens)
    tokens = stem_words(tokens)
    record_dict = dict()

    for token in tokens:
        token_frequency = record_dict[token].frequency if token in record_dict else 0
        record_dict[token] = Record(
            uuid.uuid1(), document["post_url"], token_frequency + 1)

    updated_index = {
        key: [record] if key not in index_dict else index_dict[key] + [record]
        for (key, record) in record_dict.items()
    }

    index_dict.update(updated_index)


def calculate_tf_idf():
    for key in index_dict.keys():
        df = len(index_dict[key])
        idf = log10(ndocs / df)
        for doc in index_dict[key]:
            doc.tf_idf = doc.frequency * idf


def persist_iindex(documents, input_file, output_file):
    print("Generating index...")

    # Generate Inverted Index
    doc_num = 1
    for document in documents:
        iindex(document)
        doc_num = doc_num + 1
    calculate_tf_idf()
    # Persist the Index File
    index_file = open(output_file, "wb")
    pickle.dump(index_dict, index_file)
    index_file.close()

    print("Generated {} documents".format(doc_num))


if __name__ == '__main__':
    input_file = "../data/ars-technica.json"
    output_file = "../data/ars-technica.pickle"
    with open(input_file, "r") as file:
        documents = json.load(file)

    ndocs = len(documents)

    persist_iindex(documents, input_file, output_file)
