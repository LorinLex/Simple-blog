from django.contrib.auth.models import User
from rest_framework import serializers
from posts.models import Post

class User(serializers.ModelSerializer):

    class Meta:
        fields = [
            'id',
            'first_name',
            'last_name',
            'is_stuff',
            'date_joined'
        ]
