from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from langdetect import detect


class Submission(models.Model):

    class SubmissionStatus(models.TextChoices):
        PENDING = "PND"
        PROCESSING = "PRG"
        PROCESSED = "PRD"

    user = models.ForeignKey(User, null=True, on_delete=models.RESTRICT)
    status = models.CharField(max_length=3, choices=SubmissionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Document(models.Model):

    def get_file_path(self, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join("documents/", filename)

    class DocumentType(models.TextChoices):
        FILE = "F"
        TEXT = "T"

    file = models.FileField(upload_to=get_file_path, null=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=False)
    text_raw = models.TextField(null=False)
    type = models.CharField(max_length=1, choices=DocumentType.choices)
    language = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_and_process_text(cls, submission=None, text_raw=None, file=None, language="", save=True):
        if file:
            text_raw = cls.process_file(file)
        if not text_raw:
            return None

        type = cls.DocumentType.FILE if file else cls.DocumentType.TEXT
        text = cls.process_raw_text(text_raw)

        document = cls(file=file, submission=submission, text=text, text_raw=text_raw, type=type, language=language)
        document = document.save() if save else document
        # TODO: Add document to elastic
        return document

    def __str__(self):
        return f"document-{self.id}-{self.type.label}"

    def process_file(self, file):
        # Replace with actual process file method. Returns text from file.
        return "test"

    def process_raw_text(self, text_raw):
        # Replace with actual process raw text method.
        return text_raw

    def detect_language(self, text_raw):
        return detect(text_raw)

class Result(models.Model):

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    matched_docs = models.JSONField()
    error_msg = models.TextField(null=False)
