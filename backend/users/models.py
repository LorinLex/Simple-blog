from django.db import models
from posts.models import Post, Tag
from django.contrib.auth.models import User
# Create your models here.

class UserDetail(models.Model):
    status = models.CharField(max_length=100)
    liked_tags = models.ManeToMany(Tag, blank=True)
