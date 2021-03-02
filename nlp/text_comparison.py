from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp.greedy_string_tiling import gst


def compare_two_texts(a, b, length):
    first_to_second = gst(a, b, length)
    second_to_first = gst(b, a, length)

    return (first_to_second[0], round(first_to_second[1] / len(a), 3)), \
           (second_to_first[0], round(second_to_first[1] / len(b), 3))


def compare_to_many_texts(a, files, length):
    final_intervals = []
    intervals = []
    for file in files:
        gst_list = gst(a, file, length)
        for similarity in gst_list[0]:
            add = True
            for interval in final_intervals:
                if similarity[2] in interval[2]:
                    add = False
            if add:
                intervals.append(similarity)

        final_intervals = set().union(final_intervals, intervals)
        intervals.clear()

    mask = len(a) * '*'
    for interval in final_intervals:
        mask = mask[:a.find(interval[2])] + (len(interval[2]) * '_') + mask[a.find(interval[2]) + len(interval[2]):]

    return final_intervals, round(mask.count('_')/len(a), 3)


def text_comparison(doc1, doc2):
    document_vectors = TfidfVectorizer().fit_transform([doc1, doc2])
    return cosine_similarity(document_vectors)[0][1]
