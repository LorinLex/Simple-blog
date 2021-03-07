from django.contrib import admin
from .models import Post, PostLike, PostDislike, Tag
# Register your models here.

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostDislike)
admin.site.register(Tag)
