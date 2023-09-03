from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=256)
    user = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}: {self.content}'

class Following(models.Model):
    follower = models.CharField(max_length=128)
    followee = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.follower} followed {self.followee}'

class Like(models.Model):
    postID = models.CharField(max_length=128)
    user = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.user} liked {self.postID}'