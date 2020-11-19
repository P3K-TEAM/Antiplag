from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('documents/', filename)


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    

class Document(models.Model):

    file = models.FileField(upload_to=get_file_path, null=True, blank=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.file.name



