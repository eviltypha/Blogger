from django import forms
from django.forms import fields
from .models import Post


class ImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('description', 'image', 'public')
