from django.contrib import admin
from .models import Post, Tag
# Register your models here.


class PostsWithTags(admin.TabularInline):
    model = Tag.post_set.through

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)
    inlines = [
        PostsWithTags,
    ]

admin.site.register(Post)
