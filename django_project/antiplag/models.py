from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)

    def __str__(self):
        return self.username



class Paper(models.Model):
    title = models.CharField(max_length=120)
    text = models.CharField(max_length=500, default="")
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.title


class File(models.Model):
    file = models.FileField(upload_to='papers/')
    timestamp = models.DateTimeField(auto_now_add=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)