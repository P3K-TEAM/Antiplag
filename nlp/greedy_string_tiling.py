from gst import match as match_c_ext


def greedy_string_tiling(text_a, text_b, min_length):
    matches = match_c_ext(text_a, '', text_b, '', min_length)
    similarities = []
    length = 0
    for match in matches:
        length = length + match[2]
        similarities.append({"fromA": match[0],
                             "toA": match[0] + match[2] - 1,
                             "fromB": match[1],
                             "toB": match[1] + match[2] - 1})
    return similarities, length


