from django.db import models
from posts.models import Post, Tag
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    user_img = models.ImageField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(max_length=100, blank=True)
    subscribe_tags = models.ManyToManyField(
            Tag, blank=True, related_name='subscribe_tags')
    favourite_posts = models.ManyToManyField(
            Post, blank=True, related_name='favourite_posts')
    user_posts = models.ManyToManyField(
            Post, blank=True, related_name='user_posts')
    subscribe_users = models.ManyToManyField(
            'self', blank=True, related_name='subscribe_users')
    likes = models.ManyToManyField(
            'self', blank=True, related_name='likes_from_users')
    dislikes = models.ManyToManyField(
            'self', blank=True, related_name='dislikes_from_users')
