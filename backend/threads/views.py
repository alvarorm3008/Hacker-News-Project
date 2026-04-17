from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ASWproject.utils import get_time_ago
from comments.models import Comment  # Importamos el modelo de comentarios

# Create your views here.

def threads(request):
    return render(request, 'threads/threads.html')



def user_comments(request):
    if not request.user.is_authenticated:
        # Si el usuario no está autenticado, renderizamos solo la cabecera sin comentarios
        return render(request, 'threads/threads.html')

    # Si el usuario está autenticado, cargamos sus comentarios y respuestas
    user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')
    user_replies = Comment.objects.filter(parent__author=request.user).order_by('-created_at')

    for comment in user_comments:
        comment.time_ago = get_time_ago(comment.created_at)
        comment.has_voted = comment.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        
    for reply in user_replies:
        reply.time_ago = get_time_ago(reply.created_at)
        reply.has_voted = reply.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False


    # Pasamos los comentarios y respuestas al template
    return render(request, 'threads/threads.html', {
        'user_comments': user_comments,
        'user_replies': user_replies
    })