from django.shortcuts import render
from .models import Comment
from .serializers import CommentSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from submissions.models import Submission
from .forms import CommentForm
from submissions.forms import SubmissionForm
from ASWproject.utils import get_time_ago
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication as ApiKeyAuthentication
from rest_framework import status
from rest_framework.views import APIView


# Create your views here.
    
@api_view(['GET'])
def all_comments(request):
    comments = Comment.objects.all()
    
    # Agregar metadatos a los comentarios
    for comment in comments:
        comment.time_ago = get_time_ago(comment.created_at)
        comment.has_voted = comment.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    
    # Verificar si la solicitud espera JSON (API)
    if request.headers.get('Accept') == 'application/json':
        # Serializar los comentarios
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        data = serializer.data
        return JsonResponse({'comments': data}, safe=False)

    # Caso contrario, renderizar el HTML
    return render(request, 'comments/comments.html', {'comments': comments})

def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    submission = comment.submission
    replies = comment.replies.all()
    comment.has_voted = comment.voted_by.filter(id=request.user.id).exists()
    for reply in replies:
        reply.time_ago = get_time_ago(reply.created_at)
        reply.has_voted = reply.voted_by.filter(id=request.user.id).exists()

    time_ago = get_time_ago(comment.created_at)  # Obtener el tiempo transcurrido
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.submission = submission
            reply.author = request.user
            reply.parent = comment
            reply.save()
            return redirect('comment_detail', pk=comment.pk)
    else:
        form = CommentForm()
    
    return render(request, 'comments/comment_detail.html', {
        'comment': comment,
        'submission': submission,
        'replies': replies,
        'form': form,
        'time_ago': time_ago,
    })

def reply_comment(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    submission = parent_comment.submission
    parent_comment.time_ago = get_time_ago(parent_comment.created_at)
    parent_comment.has_voted = parent_comment.voted_by.filter(id=request.user.id).exists()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.submission = submission
            comment.author = request.user
            comment.parent = parent_comment
            comment.save()
            return redirect('submission_detail', pk=submission.pk)
    else:
        comment_form = CommentForm(initial={'parent': parent_comment.id})
    
    return render(request, 'comments/reply_comment.html', {
        'submission': submission,
        'parent_comment': parent_comment,
        'comment_form': comment_form, 
    })

def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    submission = comment.submission
    time_ago = get_time_ago(comment.created_at)  # Obtener el tiempo transcurrido
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('submission_detail', pk=submission.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comments/edit_comment.html', {
        'form': form,
        'comment': comment,
        'time_ago': time_ago,
    })

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    submission = comment.submission
    time_ago = get_time_ago(comment.created_at)  # Obtener el tiempo transcurrido
    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            comment.delete()
            return redirect('submission_detail', pk=submission.pk)
        elif request.POST.get('confirm') == 'no':
            return redirect('submission_detail', pk=submission.pk)
    return render(request, 'comments/delete_comment.html', {
        'comment': comment,
        'time_ago': time_ago,
    })

@login_required
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Comprobar si el usuario ya ha votado
    if comment.voted_by.filter(id=request.user.id).exists():
        # Si ya votó, quitar el voto
        comment.voted_by.remove(request.user)
        comment.points -= 1  # Restar 1 punto
    else:
        # Si no ha votado, añadir el voto
        comment.voted_by.add(request.user)
        comment.points += 1  # Sumar 1 punto

    comment.save()  # Guardar los cambios
    next_url = request.POST.get('next', '/')
    return redirect(next_url)

@login_required
def favorite_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user in comment.favorite_by.all():
        # Si el usuario ya tiene esta publicación en sus favoritos, la elimina
        comment.favorite_by.remove(request.user)
    else:
        # Si el usuario no tiene esta publicación en sus favoritos, la agrega
        comment.favorite_by.add(request.user)

    return redirect('comment_detail', pk=comment.id) 
