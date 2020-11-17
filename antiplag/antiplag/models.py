from django.db import models
from django.contrib.auth.models import User


class Submission(models.Model):
    id = models.AutoField(primary_key=True)


class Document(models.Model):
    file = models.FileField(upload_to='documents/', null=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.file.name
