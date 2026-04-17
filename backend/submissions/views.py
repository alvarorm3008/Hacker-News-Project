from django.shortcuts import render, redirect, get_object_or_404
from .models import Submission
from comments.models import Comment
from .forms import SubmissionForm, EditSubmissionForm
from comments.forms import CommentForm
from ASWproject.utils import get_shortened_url, get_time_ago, get_num_comments
from django.contrib.auth.decorators import login_required


def submit_submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        
        if form.is_valid():
            # Obtener los datos del formulario
            url = form.cleaned_data.get('url')
            text = form.cleaned_data.get('text')
            
            # Determinar el tipo de submission
            submission_type = 'url' if url else 'ask'

            # Si es de tipo 'url', verificar si ya existe un submission con la misma URL
            if submission_type == 'url':
                existing_submission = Submission.objects.filter(url=url).first()
                if existing_submission:
                    # Redirigir a la página de detalles si existe una submission con la misma URL
                    return redirect('submission_detail', pk=existing_submission.pk)

            # Crear la nueva submission
            new_submission = form.save(commit=False)
            new_submission.author = request.user
            new_submission.submission_type = submission_type  # Guardar el tipo de submission
            new_submission.save()

            # Redirigir según el tipo de submission
            if submission_type == 'url':
                return redirect('newest')
            else:
                return redirect('ask')
    else:
        form = SubmissionForm()
    
    return render(request, 'submissions/submit.html', {'form': form})


def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    comments = submission.comments.filter(parent__isnull=True)
    shortened_url = get_shortened_url(submission.url) if submission.url else ""
    time_ago = get_time_ago(submission.created_at)  # Obtener el tiempo transcurrido
    num_comments = get_num_comments(submission)  # Obtener el número de comentarios
    submission.has_voted = submission.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    # Calcular el tiempo transcurrido para cada comentario y sus respuestas
    for comment in comments:
        comment.time_ago = get_time_ago(comment.created_at)
        comment.has_voted = comment.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        for reply in comment.replies.all():
            reply.time_ago = get_time_ago(reply.created_at)
            reply.has_voted = reply.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.submission = submission
            comment.author = request.user
            comment.save()
            return redirect('submission_detail', pk=submission.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'submissions/submission_detail.html', {
        'submission': submission,
        'comments': comments,
        'comment_form': comment_form,
        'shortened_url': shortened_url,
        'time_ago': time_ago,  # Pasamos el tiempo transcurrido al contexto
        'num_comments': num_comments,  # Pasar el número de comentarios al contexto
    })

def edit_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    shortened_url = get_shortened_url(submission.url) if submission.url else ""
    time_ago = get_time_ago(submission.created_at)  # Obtener el tiempo transcurrido
    
    if request.method == 'POST':
        form = EditSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            submission.title = request.POST.get('title')
            submission.text = request.POST.get('text')
            submission.save()
            return redirect('edit_submission', pk=submission.pk)
    else:
        form = EditSubmissionForm(instance=submission)

    return render(request, 'submissions/edit.html', {
        'submission': submission,
        'shortened_url': shortened_url,
        'time_ago': time_ago,  # Pasamos el tiempo transcurrido al contexto
        'form': form,
    })

def delete_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            submission.delete()
            return redirect('news')
        elif request.POST.get('confirm') == 'no':
                return redirect('news')
    return render(request, 'submissions/delete.html', {'submission': submission})

@login_required
def hide_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.user in submission.hidden_by.all():
        submission.hidden_by.remove(request.user)  # Un-hide
    else:
        submission.hidden_by.add(request.user)  # Hide

    # Redirigir a la página de detalles de la submission
    return redirect('submission_detail', pk=submission.id)

@login_required
def vote_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    # Comprobar si el usuario ya ha votado
    if submission.voted_by.filter(id=request.user.id).exists():
        # Si ya votó, quitar el voto
        submission.voted_by.remove(request.user)
        submission.points -= 1  # Restar 1 punto
    else:
        # Si no ha votado, añadir el voto
        submission.voted_by.add(request.user)
        submission.points += 1  # Sumar 1 punto

    submission.save()  # Guardar los cambios
    return redirect('news')  # Redirigir a la página de noticias (o donde sea adecuado)

@login_required
def favorite_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.user in submission.favorite_by.all():
        # Si el usuario ya tiene esta publicación en sus favoritos, la elimina
        submission.favorite_by.remove(request.user)
    else:
        # Si el usuario no tiene esta publicación en sus favoritos, la agrega
        submission.favorite_by.add(request.user)

    return redirect('submission_detail', pk=submission.id) 