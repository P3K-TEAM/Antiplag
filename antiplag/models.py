import uuid

from django.db import models
from django.contrib.auth.models import User
from .constants import EMAIL_ADDRESS_RFC5321_LENGTH

from antiplag.enums import SubmissionStatus, MatchType
from antiplag.managers import SubmissionManager
from antiplag.utils import merge_intervals


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)
    status = models.CharField(max_length=10, choices=SubmissionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=EMAIL_ADDRESS_RFC5321_LENGTH, null=True)

    objects = SubmissionManager()

    def __str__(self):
        return f"Submission {self.id} ({self.status})"


class Document(models.Model):
    class DocumentType(models.TextChoices):
        FILE = "FILE"
        TEXT = "TEXT"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    total_percentage = models.FloatField(null=True)

    def __str__(self):
        return f"{self.name if self.name else f'Document {self.id}'} ({self.type})"

    @property
    def ranges(self):
        indices = []

        for result in self.results.all():
            for range in result.ranges:
                indices.append(
                    {
                        "id": result.match_id,
                        "name": result.match_name,
                        "percentage": result.percentage,
                        "from": range["fromA"],
                        "to": range["toA"],
                    }
                )

        return merge_intervals(indices)


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="results"
    )
    match_id = models.CharField(max_length=255)
    match_type = models.CharField(max_length=8, choices=MatchType.choices)
    match_name = models.CharField(max_length=255)
    ranges = models.JSONField()
    percentage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.document}"
