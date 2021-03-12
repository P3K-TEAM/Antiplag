from nlp.greedy_string_tiling import gst


def compare_two_texts(a, b, length):
    first_to_second = gst(a, b, length)
    second_to_first = gst(b, a, length)

    return {"first_to_second": {"intervals": first_to_second[0], "similarity": round(first_to_second[1] / len(a), 3)},
           "second_to_first": {"intervals": second_to_first[0], "similarity": round(second_to_first[1] / len(b), 3)}}


def text_comparison(doc1, doc2):
    return compare_two_texts(doc1, doc2, 50)
