# models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Submission(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=500, blank=True, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    points = models.IntegerField(default = 1)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.TextField(blank=True, null=True, default='')
    submission_type = models.CharField(max_length=10, editable=False, default='text')

    # Many-to-Many field to track hidden submissions for each user
    hidden_by = models.ManyToManyField(User, related_name='hidden_submissions', blank=True)

    # Many-to-Many field to track who voted for this submission
    voted_by = models.ManyToManyField(User, related_name='voted_submissions', blank=True)

    # Many-to-Many field to track user's favorite submissions
    favorite_by = models.ManyToManyField(User, related_name='favorite_submissions', blank=True)



    def save(self, *args, **kwargs):
        if self.url:
            self.submission_type = 'url'
        else:
            self.submission_type = 'ask'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
