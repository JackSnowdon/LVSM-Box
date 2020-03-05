from django import forms
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['created_on', 'done_by', 'last_modified', 'views']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['post', 'created_date', 'author']
