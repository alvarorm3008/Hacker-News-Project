from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ASWproject import settings
import boto3
from news.views import calculate_relevance
from .forms import AboutForm, ProfileImageForm, ProfileBannerForm
from submissions.models import Submission
from comments.models import Comment
from django.contrib.auth.models import User
import uuid
from django.db import models
from accounts.models import Profile
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from botocore.config import Config
from allauth.account.utils import perform_login
from ASWproject.utils import get_num_comments, get_shortened_url, get_time_ago
from ASWproject.utils import calculate_karma, get_time_ago

def upload_to_s3(file, path):
    """Función auxiliar para subir archivos a S3"""
    try:
        # Configurar el cliente de S3 con la región específica
        config = Config(
            region_name=settings.AWS_S3_REGION_NAME,
            signature_version='s3v4'
        )
        
        # Crear el cliente S3 con todas las credenciales
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            config=config
        )
        
        # Subir el archivo con los parámetros correctos
        s3_client.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            path,
            ExtraArgs={  # Parámetros adicionales para el archivo
                'ContentType': getattr(file, 'content_type', 'application/octet-stream')
            }
        )
        
        # Construir la URL del archivo
        url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{path}"
        print(f"Archivo subido exitosamente a: {url}")
        return url
        
    except Exception as e:
        print(f"Error detallado al subir a S3: {str(e)}")
        return None
    
def delete_s3_file(url):
    """Función auxiliar para subir archivos a S3"""
    try:
        # Configurar el cliente de S3 con la región específica
        config = Config(
            region_name=settings.AWS_S3_REGION_NAME,
            signature_version='s3v4'
        )
        
        # Crear el cliente S3 con todas las credenciales
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            config=config
        )
        
        if settings.AWS_S3_CUSTOM_DOMAIN in url:
            path = url.split(settings.AWS_S3_CUSTOM_DOMAIN + '/')[-1]
        else:
            path = url.split('//')[-1].split('/', 1)[1]
        
        # Eliminar el archivo
        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=path
        )
        return True
    except Exception as e:
        print(f"Error eliminando archivo de S3: {str(e)}")
        return False

@login_required
def profile(request):
    user = request.user

 # Manejar eliminación de imágenes via query params
    if request.method == 'GET':
        action = request.GET.get('action')
        if action == 'delete_profile_image':
            if user.profile.imagen_perfil_url != user.profile.DEFAULT_PROFILE_IMAGE:
                delete_s3_file(user.profile.imagen_perfil_url)
                user.profile.imagen_perfil_url = user.profile.DEFAULT_PROFILE_IMAGE
                user.profile.save()
            return redirect('accounts:profile')
            
        elif action == 'delete_profile_banner':
            if user.profile.banner_perfil_url != user.profile.DEFAULT_BANNER_IMAGE:
                delete_s3_file(user.profile.banner_perfil_url)
                user.profile.banner_perfil_url = user.profile.DEFAULT_BANNER_IMAGE
                user.profile.save()
            return redirect('accounts:profile')
    
    # Si el formulario se envía (POST)
    if request.method == 'POST':
        if 'about' in request.POST:
            form = AboutForm(request.POST)
            if form.is_valid():
                user.profile.about = form.cleaned_data['about']
                user.profile.save()
                return redirect('accounts:profile')
        elif 'imagen' in request.FILES:
            form_image = ProfileImageForm(request.POST, request.FILES)
            if form_image.is_valid():
                imagen = form_image.cleaned_data['imagen']
                path = f'{user.username}_profile_{imagen.name}'
                
                # Eliminar la imagen anterior si existe y no es la default
                if user.profile.imagen_perfil_url != user.profile.DEFAULT_PROFILE_IMAGE:
                    delete_s3_file(user.profile.imagen_perfil_url)
                
                # Subir la nueva imagen
                url = upload_to_s3(imagen, path)
                if url:
                    user.profile.imagen_perfil_url = url
                    user.profile.save()
                
                return redirect('accounts:profile')      
        elif 'banner' in request.FILES:
            form_banner = ProfileBannerForm(request.POST, request.FILES)
            if form_banner.is_valid():
                banner = form_banner.cleaned_data['banner']
                path = f'{user.username}_banner_{banner.name}'
                
                # Eliminar el banner anterior si existe y no es el default
                if user.profile.banner_perfil_url != user.profile.DEFAULT_BANNER_IMAGE:
                    delete_s3_file(user.profile.banner_perfil_url)
                
                # Subir el nuevo banner
                url = upload_to_s3(banner, path)
                if url:
                    user.profile.banner_perfil_url = url
                    user.profile.save()
                
                return redirect('accounts:profile')
    else:
        form = AboutForm(initial={'about': user.profile.about})
        form_image = ProfileImageForm()
        form_banner = ProfileBannerForm()

    return render(request, 'accounts/profile.html', {
        'form': form,
        'form_image': form_image,
        'form_banner': form_banner,
        'user': user,
        'karma': calculate_karma(user),
        'api_key': user.profile.api_key,
        'author_username': user.username,
        'profile_image_url': user.profile.get_imagen_perfil,
        'profile_banner_url': user.profile.get_banner_perfil
    })

def author_submissions(request, username): ## ya en API
    # Obtener el autor por nombre de usuario
    author = get_object_or_404(User, username=username)
    # Obtener las submissions de este autor
    submissions = Submission.objects.filter(author=author)
    for submission in submissions:
        sions = Submission.objects.filter(submission_type='url').order_by('-points')

    # Excluye las submissions ocultas por el usuario autenticado
    if request.user.is_authenticated:
        submissions = submissions.exclude(hidden_by=request.user)

    for submission in submissions:
        submission.time_ago = get_time_ago(submission.created_at)
        submission.relevance = calculate_relevance(submission)
        submission.shortened_url = get_shortened_url(submission.url)
        submission.num_comments = get_num_comments(submission)  # Obtener el número de comentarios
        submission.has_voted = submission.voted_by.filter(id=request.user.id).exists()
    return render(request, 'accounts/author_submissions.html', {
        'submissions': submissions,
        'author': author,
    })

def author_comments(request, username): ## ya en API
    # Obtener el usuario basado en el nombre de usuario
    author = get_object_or_404(User, username=username)
    # Obtener los comentarios del autor
    comments = Comment.objects.filter(author=author)
    for comment in comments:
        comment.time_ago = get_time_ago(comment.created_at)
        comment.has_voted = comment.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    
    return render(request, 'accounts/author_comments.html', {
        'author': author,
        'comments': comments,
    })
    
def author_profile(request, username): ## ya en API
    # Obtener el usuario por su nombre de usuario
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    
    return render(request, 'accounts/author_profile.html', {
        'user': user,
        'profile': profile,
        'show_submissions_url': f'accounts:author_submissions',
        'author_username': username,
        'karma': calculate_karma(user),
    })


@login_required
def hidden_submissions(request): ## ya en API
    hidden_submissions = request.user.hidden_submissions.all()
    return render(request, 'accounts/hidden_submissions.html', {'hidden_submissions': hidden_submissions})

##POST
@login_required
def unhide_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    # Remueve la publicación de la lista de ocultas del usuario
    request.user.hidden_submissions.remove(submission)
    return redirect('accounts:hidden_submissions')  # Redirige a la página de hidden_submissions después de "un-hide"

@login_required
def voted_submissions(request): ## ya en API
    # Obtener las submissions votadas por el usuario logueado
    voted_submissions = request.user.voted_submissions.all()
    return render(request, 'accounts/voted_submissions.html', {
        'voted_submissions': voted_submissions,
    })

##POST
@login_required
def unvote_submission(request, submission_id):
    # Obtener la submission que el usuario desea desvotar
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Verificar si el usuario ya había votado en esta submission
    if request.user in submission.voted_by.all():
        submission.voted_by.remove(request.user)  # Eliminar el voto del usuario
        submission.points -= 1  # Decrementar los puntos de la submission
        submission.save()  # Guardar la actualización
        
    return redirect('accounts:voted_submissions')  # Redirigir a la página de submissions votadas

def favorite_submissions(request, username): ## ya en API
    author = get_object_or_404(User, username=username)
    # Obtener todas las publicaciones favoritas del usuario
    favorite_submissions = author.favorite_submissions.all()

    return render(request, 'accounts/favorite_submissions.html', {
            'favorite_submissions': favorite_submissions,
            'profile_user': author
        })

##POST
@login_required
def unfavorite_submission(request, submission_id):
    # Obtener la publicación que el usuario desea quitar de favoritos
    submission = get_object_or_404(Submission, id=submission_id)

    # Verificar si el usuario ya había agregado esta publicación a favoritos
    if request.user in submission.favorite_by.all():
        submission.favorite_by.remove(request.user)  # Quitar al usuario de favoritos
    return redirect('accounts:favorite_submissions')  # Redirigir a la página de submissions votadas

@login_required
def voted_comments(request): ## ya en API
    # Obtener los comments votadas por el usuario logueado
    voted_comments = request.user.voted_comments.all()
    for comment in voted_comments:
        comment.time_ago = get_time_ago(comment.created_at)
    return render(request, 'accounts/voted_comments.html', {
        'voted_comments': voted_comments,
    })

##POST
@login_required
def unvote_comment(request, comment_id):
    # Obtener los comments que el usuario desea desvotar
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Verificar si el usuario ya había votado en este comment
    if request.user in comment.voted_by.all():
        comment.voted_by.remove(request.user)  # Eliminar el voto del usuario
        comment.points -= 1  # Decrementar los puntos del comment
        comment.save()  # Guardar la actualización
        
    return redirect('accounts:voted_comments')  # Redirigir a la página de comments votadas


def favorite_comments(request, username): ## ya en API
    # Obtener el usuario según el username en la URL
    author = get_object_or_404(User, username=username)
    
       # Obtener los comentarios favoritos del usuario
    favorite_comments = author.favorite_comments.all()

    return render(request, 'accounts/favorite_comments.html', {
        'favorite_comments': favorite_comments,
        'profile_user': author
    })


##POST
@login_required
def unfavorite_comment(request, comment_id):
    # Obtener la publicación que el usuario desea quitar de favoritos
    comment = get_object_or_404(Comment, id=comment_id)

    # Verificar si el usuario ya había agregado esta publicación a favoritos
    if request.user in comment.favorite_by.all():
        comment.favorite_by.remove(request.user)  # Quitar al usuario de favoritos
    return redirect('accounts:favorite_comments')  # Redirigir a la página de submissions votadas

def complete_signup(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        sociallogin_data = request.session.pop('socialaccount_sociallogin', None)
        if sociallogin_data:
            sociallogin = SocialLogin.deserialize(sociallogin_data)
            user = sociallogin.user
            user.username = username
            user.save()

            user.profile.api_key = str(uuid.uuid4())
            user.profile.save()  # Guarda los cambios en el perfil
            
            complete_social_login(request, sociallogin)
            return redirect('news')
        else:
            return redirect('account_login')  # Redirige al login si no hay sociallogin en sesión
    return render(request, 'accounts/complete_signup.html')