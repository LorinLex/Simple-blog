from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
# Create your models here.

class SavedPost(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    post_id = models.OneToOneField(Post, on_delete=models.CASCADE)