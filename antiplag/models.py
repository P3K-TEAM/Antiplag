from django.db import models
from django.contrib.auth.models import User
from langdetect import detect

from nlp.text_preprocessing import extract_text_from_file, preprocess_text


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

    @classmethod
    def create_and_process_text(cls, submission=None, text_raw=None, file=None):
        # save the model
        document = cls.objects.create(
            file=file,
            name=file.name if file else "",
            submission=submission,
            type=cls.DocumentType.FILE if file else cls.DocumentType.TEXT,
            language=cls.detect_language(text_raw) if text_raw else None,
            text_raw=text_raw,
        )

        # asynchronously extract text from file and update the model
        if file:
            document.text_raw = document.process_file()
            document.save()

        # asynchronously preprocess raw text and update the model
        document.text = document.process_raw_text()
        print(document.text)
        document.save()

    def __str__(self):
        return f"{self.name if self.name else f'Document {self.id}'} ({self.type})"

    def process_file(self):
        return extract_text_from_file(self.file.path)

    def process_raw_text(self):
        os.environ["w2n.lang"] = self.language
        return preprocess_text(self.text_raw, words_to_numbers=True, remove_numbers=False, tokenize_words=False,
                               lemmatize=False, remove_stopwords=True)

    @staticmethod
    def detect_language(text_raw):
        return detect(text_raw)


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
