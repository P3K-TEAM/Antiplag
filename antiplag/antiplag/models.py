from django.db import models
from django.contrib.auth.models import User

class Paper(models.Model):
    title = models.CharField(max_length=120)
    #text = models.CharField(max_length=500, default="")
    file = models.FileField(upload_to='papers/', null=True)
    #timestamp = models.DateTimeField(auto_now_add=True, null=True)
    #user = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.title
