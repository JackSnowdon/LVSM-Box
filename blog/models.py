from django.db import models
from accounts.models import Profile

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    done_by = models.ForeignKey(Profile, related_name='posts', on_delete=models.PROTECT)
    views = models.IntegerField(default=1)
    CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    content_level = models.IntegerField(
        choices=CHOICES, default="1")
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(Profile, related_name='comments', on_delete=models.PROTECT)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
