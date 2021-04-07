from django.db import models
from django.contrib.auth.models import User

from antiplag.enums import SubmissionStatus
from antiplag.managers import SubmissionManager
from antiplag.utils import merge_intervals


class Submission(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)
    status = models.CharField(max_length=10, choices=SubmissionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SubmissionManager()

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
            for match in matched_doc["intervals"]:
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
