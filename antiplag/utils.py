def merge_intervals(indices):

    if len(indices) <= 0:
        return indices

    stack = []

    sorted_indices = sorted(
        indices, key=lambda x: (x["id"], x["name"], x["from"], x["to"])
    )

    stack.append(sorted_indices[0])
    sorted_indices.pop(0)

    for index in sorted_indices:
        top = stack[len(stack) - 1]

        if index["id"] != top["id"]:
            top = index
            stack.append(top)
        if top["to"] < index["from"]:
            stack.append(index)
        elif top["to"] <= index["to"]:
            top["to"] = index["to"]
            stack.pop()
            stack.append(top)

    starts = []
    ends = []

    for interval in stack:
        starts.append(
            {
                "intervals": [interval["from"], 1],
                "doc": {
                    "id": interval["id"],
                    "name": interval["name"],
                    "percentage": interval["percentage"],
                },
            }
        )
        ends.append(
            {
                "intervals": [interval["to"] + 1, -1],
                "doc": {
                    "id": interval["id"],
                    "name": interval["name"],
                    "percentage": interval["percentage"],
                },
            }
        )

    size_of_starts = len(starts)
    size_of_ends = len(ends)

    sorted_positions = []
    i, j = 0, 0

    while i < size_of_starts and j < size_of_ends:
        if starts[i]["intervals"][0] < ends[j]["intervals"][0]:
            sorted_positions.append(starts[i])
            i += 1
        else:
            sorted_positions.append(ends[j])
            j += 1

    sorted_positions = sorted_positions + starts[i:] + ends[j:]
    sorted_positions.sort(key=lambda x: x["intervals"][0], reverse=False)

    intervals = []
    docs = []
    prev = -1
    count = 0

    for interval in sorted_positions:
        if interval["intervals"][0] > prev and count != 0:
            intervals.append(
                {
                    "ranges": {"from": prev, "to": interval["intervals"][0] - 1},
                    "matches": docs[:],
                }
            )

        prev = interval["intervals"][0]
        count += interval["intervals"][1]

        if interval["intervals"][1] == 1:
            docs.append(interval["doc"])
        else:
            del docs[docs.index(interval["doc"])]

    return intervals
