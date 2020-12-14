from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def text_comparison(doc1, doc2):
    document_vectors = TfidfVectorizer().fit_transform([doc1, doc2])
    return cosine_similarity(document_vectors)[0][1]
