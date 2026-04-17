from django.utils import timezone
from django.db import models
from submissions.models import Submission
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    points = models.IntegerField(default = 1)
    created_at = models.DateTimeField(default=timezone.now)

    # Many-to-Many field to track who voted for this comment
    voted_by = models.ManyToManyField(User, related_name='voted_comments', blank=True)

    # Many-to-Many field to track user's favorite comments
    favorite_by = models.ManyToManyField(User, related_name='favorite_comments', blank=True)

 
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.submission}'
