from django.db import models
from django.contrib.auth.models import User


class Submission(models.Model):
    title = models.CharField(max_length=100)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #timestamp = models.DateTimeField(auto_now_add=True, null=True)


class Paper(models.Model):
    #text = models.CharField(max_length=500, default="")
    photo = models.FileField(upload_to='papers/', null=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='paper', default=0)
    def __str__(self):
        return self.file.name
