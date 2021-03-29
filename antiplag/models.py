from django.db import models
from django.contrib.auth.models import User


class Submission(models.Model):
    class SubmissionStatus(models.TextChoices):
        PENDING = "PENDING"
        PROCESSING = "PROCESSING"
        PROCESSED = "PROCESSED"

    user = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)
    status = models.CharField(max_length=10, choices=SubmissionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission {self.id} ({self.status})"


class Document(models.Model):
    class DocumentType(models.TextChoices):
        FILE = "FILE"
        TEXT = "TEXT"

    file = models.FileField(upload_to="documents/", null=True)
    name = models.CharField(max_length=255, blank=True)
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, null=True, related_name="documents"
    )
    text = models.TextField(null=True)
    text_raw = models.TextField(null=True)
    type = models.CharField(max_length=4, choices=DocumentType.choices)
    language = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name if self.name else f'Document {self.id}'} ({self.type})"


def merge_intervals(indices):

    if len(indices) <= 1:
        return indices

    stack = []

    sorted_indices = sorted(indices, key=lambda x: (x['id'], x['name'], x['from'], x['to']))

    stack.append(sorted_indices[0])
    sorted_indices.pop(0)

    for x in sorted_indices:

        top = stack[len(stack) - 1]

        if x['id'] != top['id']:
            top = x
            stack.append(top)

        if top['to'] < x['from']:
            stack.append(x)

        elif top['to'] <= x['to']:
            top['to'] = x['to']
            stack.pop()
            stack.append(top)

    starts = []
    for x in stack:
        starts.append(
            {
                "intervals": [x['from'], 1],
                "doc": {
                    "id": x['id'],
                    "name": x['name'],
                    "percentage": x['percentage']
                }
            }
        )

    ends = []
    for x in stack:
        ends.append(
            {
                "intervals": [x['to'] + 1, -1],
                "doc": {
                    "id": x['id'],
                    "name": x['name'],
                    "percentage": x['percentage']
                }
            }
        )

    size_1 = len(starts)
    size_2 = len(ends)

    sorted_positions = []
    i, j = 0, 0

    while i < size_1 and j < size_2:
        if starts[i]['intervals'][0] < ends[j]['intervals'][0]:
            sorted_positions.append(starts[i])
            i += 1

        else:
            sorted_positions.append(ends[j])
            j += 1

    sorted_positions = sorted_positions + starts[i:] + ends[j:]
    sorted_positions.sort(key=lambda x: x['intervals'][0], reverse=False)

    intervals = []
    docs = []
    prev = -1
    count = 0

    for x in sorted_positions:
        if x['intervals'][0] > prev and count != 0:
            intervals.append(
                {
                    'ranges': {
                        "from": prev,
                        "to": x['intervals'][0] - 1
                    },
                    'matches': docs[:]
                }
            )

        prev = x['intervals'][0]
        count += x['intervals'][1]

        if x['intervals'][1] == 1:
            docs.append(x['doc'])

        else:
            del docs[docs.index(x['doc'])]

    return intervals


class Result(models.Model):
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, related_name="result"
    )
    matched_docs = models.JSONField()
    percentage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.document}"

    @property
    def matches(self):
        return len(self.matched_docs)

    @property
    def intervals(self):

        indices = []

        for matched_doc in self.matched_docs:
            for match in matched_doc['intervals']:
                indices.append(
                    {
                        "id": self.matched_docs.index(matched_doc),
                        "name": matched_doc["name"],
                        "percentage": matched_doc["percentage"],
                        "from": match["fromA"],
                        "to": match["toA"],
                    }
                )

        merged_intervals = merge_intervals(indices)

        return merged_intervals

