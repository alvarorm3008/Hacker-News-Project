from urllib.parse import urlparse
from django.utils.timezone import now
from datetime import timedelta
from django.db import models

from comments.models import Comment
from submissions.models import Submission

def get_shortened_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc  # Devuelve solo el dominio

def get_time_ago(created_at):
    time_diff = now() - created_at
    if time_diff < timedelta(minutes=1):
        return "just now"
    elif time_diff < timedelta(hours=1):
        return f"{int(time_diff.total_seconds() // 60)} minutes ago"
    elif time_diff < timedelta(days=1):
        return f"{int(time_diff.total_seconds() // 3600)} hours ago"
    else:
        return f"{time_diff.days} days ago"

def get_num_comments(submission):
    num_comments = submission.comments.count()  # Obtener el número de comentarios
    if (num_comments == 0): return "discuss"
    elif (num_comments == 1): return "1 comment"
    else: 
        return f"{num_comments} comments"
    
def calculate_karma(user):
    submissions_points = Submission.objects.filter(author=user).aggregate(total_points=models.Sum('points'))['total_points'] or 0
    comments_points = Comment.objects.filter(author=user).aggregate(total_points=models.Sum('points'))['total_points'] or 0
    karma = submissions_points + comments_points
    if karma < 1:
        karma = 1
    user.profile.karma = karma
    return karma   