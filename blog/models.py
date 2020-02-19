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