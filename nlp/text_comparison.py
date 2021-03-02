from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp.greedy_string_tiling import gst


def gst_compare_two_texts(a, b, length):
    first_to_second = gst(a, b, length)
    second_to_first = gst(b, a, length)
    similar_chars = 0

    print(first_to_second)
    for similarity in first_to_second:
        similar_chars += len(similarity)

    similar_chars = 0
    print(second_to_first)
    for similarity in second_to_first:
        similar_chars += len(similarity)

    return similar_chars / len(a), similar_chars / len(b)


def gst_compare_to_many_texts(a, files, length):
    final_intervals = []
    intervals = []
    for file in files:
        gst_list = gst(a, file, length)
        for similarity in gst_list:
            add = True
            for interval in final_intervals:
                if similarity in interval:
                    add = False
            if add:
                intervals.append(similarity)

        final_intervals = set().union(final_intervals, intervals)
        intervals.clear()

    mask = len(a) * '*'
    for interval in final_intervals:
        mask = mask[:a.find(interval)] + (len(interval) * '_') + mask[a.find(interval) + len(interval):]

    return mask.count('_')/len(a)


def text_comparison(doc1, doc2):
    document_vectors = TfidfVectorizer().fit_transform([doc1, doc2])
    return cosine_similarity(document_vectors)[0][1]
