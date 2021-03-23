from django.db import models
from posts.models import Post
from django.conf import settings

# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creation_data = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Comment_like', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Comment_dislike', blank=True)

    def __str__(self):
        return self.text[:10] + '...'
