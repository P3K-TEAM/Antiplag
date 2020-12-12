import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


def text_comparison(doc1, doc2):
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

    doc1_vector = vectorize(doc1)
    doc2_vector = vectorize(doc2)

    return similarity(doc1_vector, doc2_vector)[0][1]

