def merge_intervals(indices):

    if len(indices) <= 1:
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

    for item in stack:
        starts.append(
            {
                "intervals": [item["from"], 1],
                "doc": {
                    "id": item["id"],
                    "name": item["name"],
                    "percentage": item["percentage"],
                },
            }
        )
        ends.append(
            {
                "intervals": [item["to"] + 1, -1],
                "doc": {
                    "id": item["id"],
                    "name": item["name"],
                    "percentage": item["percentage"],
                },
            }
        )

    size_1 = len(starts)
    size_2 = len(ends)

    sorted_positions = []
    i, j = 0, 0

    while i < size_1 and j < size_2:
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

    for item in sorted_positions:
        if item["intervals"][0] > prev and count != 0:
            intervals.append(
                {
                    "ranges": {"from": prev, "to": item["intervals"][0] - 1},
                    "matches": docs[:],
                }
            )

        prev = item["intervals"][0]
        count += item["intervals"][1]

        if item["intervals"][1] == 1:
            docs.append(item["doc"])
        else:
            del docs[docs.index(item["doc"])]

    return intervals
