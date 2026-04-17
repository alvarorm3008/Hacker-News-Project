from django.shortcuts import render
from submissions.models import Submission
from ASWproject.utils import get_time_ago, get_shortened_url, get_num_comments
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from rest_framework.decorators import api_view
from django.http import JsonResponse
from submissions.serializers import SubmissionSerializer


def newest(request):
    query = request.GET.get('query', '')

    if query:
        submissions = Submission.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        submissions = Submission.objects.order_by('-created_at')

    if request.user.is_authenticated:
        # Excluye las submissions que han sido ocultadas por el usuario
        submissions = submissions.exclude(hidden_by=request.user)

    for submission in submissions:
        submission.time_ago = get_time_ago(submission.created_at)
        submission.shortened_url = get_shortened_url(submission.url)
        submission.num_comments = get_num_comments(submission)
        submission.has_voted = submission.voted_by.filter(id=request.user.id).exists()


    return render(request, 'newest/newest.html', {'submissions': submissions, 'query': query})


@login_required
def newest_hide_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    submission.hidden_by.add(request.user)  # Añade al usuario actual a la lista de ocultadores
    return redirect('newest')  # Redirige a la página de noticias después de ocultar la publicación

@login_required
def vote_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    # Si el usuario ya ha votado, lo eliminamos de la lista de votantes y restamos puntos
    if submission.voted_by.filter(id=request.user.id).exists():
        submission.voted_by.remove(request.user)
        submission.points -= 1
    else:
        # Si no ha votado, lo agregamos a la lista de votantes y sumamos puntos
        submission.voted_by.add(request.user)
        submission.points += 1

    submission.save()  # Guardar los cambios
    return redirect('newest')  # Redirigir de vuelta a la página de noticias