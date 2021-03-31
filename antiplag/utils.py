def merge_intervals(indices):

    if len(indices) <= 1:
        return indices

    stack = []

    sorted_indices = sorted(
        indices, key=lambda x: (x["id"], x["name"], x["from"], x["to"])
    )

    stack.append(sorted_indices[0])
    sorted_indices.pop(0)

    for x in sorted_indices:

        top = stack[len(stack) - 1]

        if x["id"] != top["id"]:
            top = x
            stack.append(top)

        if top["to"] < x["from"]:
            stack.append(x)

        elif top["to"] <= x["to"]:
            top["to"] = x["to"]
            stack.pop()
            stack.append(top)

    starts = []
    for x in stack:
        starts.append(
            {
                "intervals": [x["from"], 1],
                "doc": {
                    "id": x["id"],
                    "name": x["name"],
                    "percentage": x["percentage"],
                },
            }
        )

    ends = []
    for x in stack:
        ends.append(
            {
                "intervals": [x["to"] + 1, -1],
                "doc": {
                    "id": x["id"],
                    "name": x["name"],
                    "percentage": x["percentage"],
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

    for x in sorted_positions:
        if x["intervals"][0] > prev and count != 0:
            intervals.append(
                {
                    "ranges": {"from": prev, "to": x["intervals"][0] - 1},
                    "matches": docs[:],
                }
            )

        prev = x["intervals"][0]
        count += x["intervals"][1]

        if x["intervals"][1] == 1:
            docs.append(x["doc"])

        else:
            del docs[docs.index(x["doc"])]

    return intervals
