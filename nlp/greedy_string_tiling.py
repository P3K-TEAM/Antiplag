from gst import match as find_matches


def greedy_string_tiling(text_a, text_b, min_length):

    similarities = []
    length = 0

    if len(text_a) < min_length or len(text_b) < min_length:
        return similarities, 0

    matches = find_matches(text_a, '', text_b, '', min_length)

    for match in matches:
        length = length + match[2]
        similarities.append({"fromA": match[0],
                             "toA": match[0] + match[2],
                             "fromB": match[1],
                             "toB": match[1] + match[2]})
    return similarities, length


