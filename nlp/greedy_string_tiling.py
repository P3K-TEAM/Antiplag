def mark(marks, num):
    marks[num] = '_'
    return marks


def unmarked(marks, num):
    if marks[num] == '*':
        return True
    else:
        return False


def unmarked_in_range(marks, start, end):
    for i in range(start, end+1):
        if not unmarked(marks, i):
            return False
    return True


def mark(marks, num):
    marks[num] = '_'
    return marks


def gst(text_a, text_b, min_length):
    length_of_tokens_tiled = 0
    marks_a = len(text_a) * '*'
    marks_b = len(text_b) * '*'
    matches = []
    similarities = []
    while True:
        maxmatch = min_length
        for p in range(0, len(text_a)):
            for t in range(0, len(text_b)):
                j = 0
                while (p+j < len(text_a)) and \
                        (t+j < len(text_b)) and \
                        (text_a[p+j] == text_b[t+j]) and \
                        (unmarked(marks_a, p+j)) and \
                        (unmarked(marks_b, t+j)):
                    j += 1
                if j == maxmatch:
                    matches.append((j, p, t))
                elif j > maxmatch:
                    matches.append((j, p, t))
                    maxmatch = j
        for match in matches:
            if match[0] == maxmatch:
                if unmarked_in_range(marks_a, match[1], match[1] + maxmatch - 1) & \
                        unmarked_in_range(marks_b, match[2], match[2] + maxmatch - 1):
                    for j in range(0, maxmatch):
                        marks_a = mark(list(marks_a), match[1]+j)
                        marks_b = mark(list(marks_b), match[2]+j)
                    similarities.append({"begin": match[1],
                                         "end": match[1] + maxmatch})
                    length_of_tokens_tiled = length_of_tokens_tiled + maxmatch

        if maxmatch == min_length:
            break
        
    return similarities, length_of_tokens_tiled
