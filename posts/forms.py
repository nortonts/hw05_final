from django import forms
from django.forms import ModelForm
from .models import Post, Group


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "group"]
        labels = {
            "text": "Текст публикации",
            "group": "Группа"
        }

        help_texts = {
            "text": "Текст нового поста",
            "group": "Группа, к которой будет относиться пост"
        }
