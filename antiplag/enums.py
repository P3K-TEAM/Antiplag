from django.db import models


class SubmissionStatus(models.TextChoices):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
