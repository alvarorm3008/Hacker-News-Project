from django.shortcuts import render
from submissions.models import Submission
from ASWproject.utils import get_time_ago, get_shortened_url, get_num_comments
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from math import log
from django.http import JsonResponse

from submissions.serializers import SubmissionSerializer
from rest_framework.decorators import api_view

def news(request):
    # Obtiene el término de búsqueda de la solicitud GET, si existe
    query = request.GET.get('query', '')

    # Si hay una búsqueda, filtra las submissions que contengan la palabra clave en el título
    if query:
        submissions = Submission.objects.filter(submission_type='url', title__icontains=query).order_by('-points')
    else:
        # Si no hay búsqueda, muestra todas las submissions ordenadas por puntos
        submissions = Submission.objects.filter(submission_type='url').order_by('-points')

    # Excluye las submissions ocultas por el usuario autenticado
    if request.user.is_authenticated:
        submissions = submissions.exclude(hidden_by=request.user)

    for submission in submissions:
        submission.time_ago = get_time_ago(submission.created_at)
        submission.relevance = calculate_relevance(submission)
        submission.shortened_url = get_shortened_url(submission.url)
        submission.num_comments = get_num_comments(submission)  # Obtener el número de comentarios
        submission.has_voted = submission.voted_by.filter(id=request.user.id).exists()

        
    # Ordena las submissions por relevancia
    submissions = sorted(submissions, key=lambda s: s.relevance, reverse=True)

    # Pasamos la lista de submissions y el query (si existe) al template
    return render(request, 'news/news.html', {'submissions': submissions, 'query': query})

# Calcula la relevancia de una publicación en función de su antigüedad y puntos
# 1. Las submission estaran ordenadas de mas recientes a mas antiguas.
# 2. Las submission estaran ordenadas por puntos. 
# 3. Si una submission que es de 6 o menos dias tiene mas puntos que otras mas recientes, tiene las relevancia. 
# 4. Si hay una submission muy antigua (mas de 6 dias), y la votas, tendrá menos relevancia.
def calculate_relevance(submission):
    from datetime import datetime, timezone

    # Calcula la antigüedad en días
    age_in_days = (datetime.now(timezone.utc) - submission.created_at).total_seconds() / (3600 * 24)
    if age_in_days <= 6:
        # Publicaciones recientes (≤6 días)
        return submission.points + (6 - age_in_days) * 0.1  # Penalización suave por antigüedad
    else:
        # Publicaciones antiguas (>6 días)
        return submission.points / (age_in_days ** 1.5)  # Penalización significativa por antigüedad

@login_required
def news_hide_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    submission.hidden_by.add(request.user)  # Añade al usuario actual a la lista de ocultadores
    return redirect('news')  # Redirige a la página de noticias después de ocultar la publicación

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
    next_url = request.POST.get('next', '/')
    return redirect(next_url)