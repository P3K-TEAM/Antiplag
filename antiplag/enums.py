from django.db import models


class SubmissionStatus(models.TextChoices):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class MatchType(models.TextChoices):
    CORPUS = "CORPUS"
    UPLOADED = "UPLOADED"
