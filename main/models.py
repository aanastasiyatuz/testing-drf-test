from django.db import models
from account.models import User


class Post(models.Model):
    author = models.ForeignKey(User, models.CASCADE, related_name='posts')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
