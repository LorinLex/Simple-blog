from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    creation_data = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    tags_id = models.ManyToManyField(Tag, blank=True)
    likes = models.ManyToManyField(User, related_name='Post_like', blank=True)
    dislikes = models.ManyToManyField(User, related_name='Post_dislike', blank=True)
    def __str__(self):
        return self.title[:10] + '...' if len(self.title) > 10 else self.title
