import time
from news.views import calculate_relevance
from submissions.models import Submission
from comments.models import Comment
from accounts.models import Profile
from ASWproject.utils import get_time_ago, get_shortened_url, get_num_comments
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import ProfileSerializer
from ASWproject.utils import calculate_karma
from accounts.views import upload_to_s3, delete_s3_file
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from submissions.serializers import SubmissionAskSerializer, SubmissionSerializer, SubmissionCreateSerializer
from submissions.serializers import SubmissionUpdateSerializer, SubmissionDetailSerializer
from comments.serializers import CommentTreeSerializer, CommentCreateSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError
from ASWproject.utils import get_time_ago, get_shortened_url, get_num_comments
from ask.views import calculate_relevance

class NewsApi (APIView):
    def get(self, request):
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
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists()
            
        # Ordena las submissions por relevancia
        submissions = sorted(submissions, key=lambda s: s.relevance, reverse=True)

        
        serializer = SubmissionSerializer(submissions, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

##usuario
class AuthorSubmissionsAPI(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        submissions = Submission.objects.filter(author=user)
        for submission in submissions:
            submission.time_ago = get_time_ago(submission.created_at)
            submission.num_comments = get_num_comments(submission)
            submission.has_voted = submission.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        serializer = SubmissionSerializer(submissions, many=True, context={'request': request})
        return Response(serializer.data)

class AuthorCommentsAPI(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        comments = Comment.objects.filter(author=user)
        for comment in comments:
            comment.time_ago = get_time_ago(comment.created_at)
            comment.has_voted = comment.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
            comment.is_favorite = comment.favorite_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class AuthorProfileAPI(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        karma = calculate_karma(user)
        data = {
            'username': username,
            'karma': karma,
            'about': profile.about,
            'created_at': user.date_joined,
        }
        return Response(data)
    
class AuthorFavoriteSubmissionsAPI(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        favorite_submissions = user.favorite_submissions.all()
        for submission in favorite_submissions:
            submission.time_ago = get_time_ago(submission.created_at)
            submission.num_comments = get_num_comments(submission)
            submission.has_voted = submission.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        serializer = SubmissionSerializer(favorite_submissions, many=True, context={'request': request})
        return Response(serializer.data)

class AuthorFavoriteCommentsAPI(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        favorite_comments = user.favorite_comments.all()
        for comment in favorite_comments:
            comment.time_ago = get_time_ago(comment.created_at)
            comment.has_voted = comment.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
            comment.is_favorite = comment.favorite_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        serializer = CommentSerializer(favorite_comments, many=True, context={'request': request})
        return Response(serializer.data)
    
class HiddenSubmissionsApi (APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        hidden_submissions = request.user.hidden_submissions.all()
        for submission in hidden_submissions:
            submission.time_ago = get_time_ago(submission.created_at)
            submission.num_comments = get_num_comments(submission)
            submission.has_voted = submission.voted_by.filter(id=request.user.id).exists()
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists()
        serializer = SubmissionSerializer(hidden_submissions, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

class VotedSubmissionsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        voted_submissions = request.user.voted_submissions.all()
        for submission in voted_submissions:
            submission.time_ago = get_time_ago(submission.created_at)
            submission.num_comments = get_num_comments(submission)
            submission.has_voted = submission.voted_by.filter(id=request.user.id).exists()
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists()
        serializer = SubmissionSerializer(voted_submissions, many=True, context={'request': request})
        return Response(serializer.data)

        
class FavoriteSubmissionsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        favorite_submissions = request.user.favorite_submissions.all()
        for submission in favorite_submissions:
            submission.time_ago = get_time_ago(submission.created_at)
            submission.num_comments = get_num_comments(submission)
            submission.has_voted = submission.voted_by.filter(id=request.user.id).exists()
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists()
        serializer = SubmissionSerializer(favorite_submissions, many=True, context={'request': request})
        return Response(serializer.data)
    

class VotedCommentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        voted_comments = request.user.voted_comments.all()
        for comment in voted_comments:
            comment.time_ago = get_time_ago(comment.created_at)
            comment.has_voted = comment.voted_by.filter(id=request.user.id).exists()
            comment.is_favorite = comment.favorite_by.filter(id=request.user.id).exists()
        serializer = CommentSerializer(voted_comments, many=True)
        return Response(serializer.data)
          

class FavoriteCommentsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        favorite_comments = request.user.favorite_comments.all()
        for comment in favorite_comments:
            comment.time_ago = get_time_ago(comment.created_at)
            comment.has_voted = comment.voted_by.filter(id=request.user.id).exists()
            comment.is_favorite = comment.favorite_by.filter(id=request.user.id).exists()
        serializer = CommentSerializer(favorite_comments, many=True, context={'request': request})
        return Response(serializer.data)
    

class ProfileDetailAPI(APIView):
    """API para consultar perfil"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def post(self, request):
        try:
            profile = request.user.profile
            updated_fields = []

            # Actualizar "about" si está presente
            about = request.data.get('about', None)
            if about is not None:
                profile.about = about
                updated_fields.append('about')

            # Actualizar imagen de perfil si está presente
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                file_name = f'profiles/{request.user.username}_profile_{int(time.time())}.{imagen.name.split(".")[-1]}'

                # Eliminar imagen anterior si no es la predeterminada
                if profile.imagen_perfil_url != profile.DEFAULT_PROFILE_IMAGE:
                    delete_s3_file(profile.imagen_perfil_url)

                url = upload_to_s3(imagen, file_name)
                if url:
                    profile.imagen_perfil_url = url
                    updated_fields.append('imagen')
                else:
                    return Response({'error': 'Error al subir la imagen de perfil'}, status=500)

            # Actualizar banner si está presente
            if 'banner' in request.FILES:
                banner = request.FILES['banner']
                file_name = f'banners/{request.user.username}_banner_{int(time.time())}.{banner.name.split(".")[-1]}'

                # Eliminar banner anterior si no es el predeterminado
                if profile.banner_perfil_url != profile.DEFAULT_BANNER_IMAGE:
                    delete_s3_file(profile.banner_perfil_url)

                url = upload_to_s3(banner, file_name)
                if url:
                    profile.banner_perfil_url = url
                    updated_fields.append('banner')
                else:
                    return Response({'error': 'Error al subir el banner'}, status=500)

            # Guardar los cambios en el perfil
            if updated_fields:
                profile.save()
                serializer = ProfileSerializer(profile)
                return Response({
                    'message': 'Perfil actualizado exitosamente',
                    'updated_fields': updated_fields,
                    'profile': serializer.data
                })

            return Response({'message': 'No se proporcionaron datos para actualizar'}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


class DeleteProfileMediaAPI(APIView):
    """API para eliminar imagen de perfil o banner"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, media_type):
        try:
            profile = request.user.profile

            if media_type == 'image':
                # Eliminar imagen de perfil
                if profile.imagen_perfil_url != profile.DEFAULT_PROFILE_IMAGE:
                    delete_s3_file(profile.imagen_perfil_url)
                    profile.imagen_perfil_url = profile.DEFAULT_PROFILE_IMAGE
                    profile.save()
                    serializer = ProfileSerializer(profile)
                    return Response({
                        'message': 'Imagen eliminada exitosamente',
                        'profile': serializer.data
                    })
                return Response({'message': 'No hay imagen personalizada para eliminar'})
            
            elif media_type == 'banner':
                # Eliminar banner
                if profile.banner_perfil_url != profile.DEFAULT_BANNER_IMAGE:
                    delete_s3_file(profile.banner_perfil_url)
                    profile.banner_perfil_url = profile.DEFAULT_BANNER_IMAGE
                    profile.save()
                    serializer = ProfileSerializer(profile)
                    return Response({
                        'message': 'Banner eliminado exitosamente',
                        'profile': serializer.data
                    })
                return Response({'message': 'No hay banner personalizado para eliminar'})
            
            return Response({'message': 'Tipo de medio no válido'}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


class CommentsAPI(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        for comment in comments:
            comment.time_ago = get_time_ago(comment.created_at)
            comment.has_voted = comment.voted_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
            comment.is_favorite = comment.favorite_by.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentDetailAPI(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        submission = comment.submission
        
        # Usar el TreeSerializer para obtener la estructura anidada
        serializer = CommentTreeSerializer(comment, context={'request': request})
        
        data = {
            'submission': {
                'id': submission.id,
                'title': submission.title
            },
            'comment': serializer.data,
        }
        return Response(data)
    
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        # Verificar que el usuario es el autor
        if comment.author != request.user:
            return Response({
                'error': 'No tienes permiso para eliminar este comentario'
            }, status=status.HTTP_403_FORBIDDEN)
            
        comment.delete()
        return Response({
            'message': 'Comentario eliminado exitosamente'
        }, status=status.HTTP_204_NO_CONTENT)
    
    
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            reply = serializer.save(
                submission=comment.submission,
                author=request.user,
                parent=comment
            )
            # Retornar el árbol actualizado
            tree_serializer = CommentTreeSerializer(comment, context={'request': request})
            return Response(tree_serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReplyCommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        parent_comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Crear el nuevo comentario
            reply = serializer.save(
                submission=parent_comment.submission,
                author=request.user,
                parent=parent_comment
            )
            
            # Obtener el árbol actualizado del comentario padre
            tree_serializer = CommentTreeSerializer(parent_comment, context={'request': request})
            
            data = {
                'comment': tree_serializer.data,
                'submission': {
                    'id': parent_comment.submission.id,
                    'title': parent_comment.submission.title
                }
            }
            return Response(data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditCommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        # Verificar que el usuario es el autor
        if comment.author != request.user:
            return Response({
                'error': 'No tienes permiso para editar este comentario'
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Comentario actualizado exitosamente',
                'comment': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteCommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, comment_id):
        """Añadir un voto a un comentario."""
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.author == request.user:
            raise ValidationError({"detail": "You cannot vote on your own submission."})
        
        if not comment.voted_by.filter(id=request.user.id).exists():
            comment.voted_by.add(request.user)
            comment.points += 1
            comment.save()
        
        # Serializar el comentario actualizado
        serializer = CommentSerializer(comment, context={'request': request})
        
        return Response({
            'points': comment.points,
            'comment': serializer.data
        })

    def delete(self, request, comment_id):
        """Quitar un voto de un comentario."""
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.voted_by.filter(id=request.user.id).exists():
            comment.voted_by.remove(request.user)
            comment.points -= 1
            comment.save()
        
        # Serializar el comentario actualizado
        serializer = CommentSerializer(comment, context={'request': request})
        
        return Response({
            'points': comment.points,
            'comment': serializer.data
        })


class FavoriteCommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, comment_id):
        """Añadir un comentario a favoritos."""
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.user not in comment.favorite_by.all():
            comment.favorite_by.add(request.user)
            comment.save()
            
            # Serializar el comentario actualizado
            serializer = CommentTreeSerializer(comment, context={'request': request})
            
            return Response({
                'status': 'Comment added to favorites',
                'comment': serializer.data
            })
        else:
            return Response({
                'status': 'Comment already in favorites'
            }, status=400)

    def delete(self, request, comment_id):
        """Eliminar un comentario de favoritos."""
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.user in comment.favorite_by.all():
            comment.favorite_by.remove(request.user)
            comment.save()
            
            # Serializar el comentario actualizado
            serializer = CommentTreeSerializer(comment, context={'request': request})
            
            return Response({
                'status': 'Comment removed from favorites',
                'comment': serializer.data
            })
        else:
            return Response({
                'status': 'Comment not in favorites'
            }, status=400)

    
class AskAPI(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve 'ask' type submissions",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Search term to filter submissions by title", type=openapi.TYPE_STRING)
        ],
        responses={200: 'A JSON response containing the list of ask type submissions'}
    )
    def get(self, request):
        # Obtiene el término de búsqueda de la solicitud GET, si existe
        query = request.GET.get('query', '')

        # Si hay una búsqueda, filtra las submissions que contengan la palabra clave en el título
        if query:
            submissions = Submission.objects.filter(submission_type='ask', title__icontains=query).order_by('-points')
        else:
            # Si no hay búsqueda, muestra todas las submissions ordenadas por puntos
            submissions = Submission.objects.filter(submission_type='ask').order_by('-points')
        
        if request.user.is_authenticated:
            # Excluye las submissions que han sido ocultadas por el usuario
            submissions = submissions.exclude(hidden_by=request.user)

        for submission in submissions:
            submission.time_ago = get_time_ago(submission.created_at)
            submission.relevance = calculate_relevance(submission)
            submission.num_comments = get_num_comments(submission)  # Obtener el número de comentarios
            submission.has_voted = submission.voted_by.filter(id=request.user.id).exists()
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists()

        # Ordena las submissions por relevancia
        submissions = sorted(submissions, key=lambda s: s.relevance, reverse=True)

     
        serializer = SubmissionAskSerializer(submissions, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    

class NewestAPI(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the newest submissions",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Search term to filter submissions by title", type=openapi.TYPE_STRING)
        ],
        responses={200: 'A JSON response containing the list of newest submissions'}
    )
    def get(self, request):
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
            submission.is_favorite = submission.favorite_by.filter(id=request.user.id).exists()

        serializer = SubmissionSerializer(submissions, many=True, context={'request': request})
        return JsonResponse({'submissions': serializer.data}, safe=False)
    
class ThreadsAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request, *args, **kwargs):
        # Cargar los comentarios del usuario y las respuestas
        user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')

        # Añadir los campos necesarios
        for comment in user_comments:
            comment.time_ago = get_time_ago(comment.created_at)
            comment.has_voted = comment.voted_by.filter(id=request.user.id).exists()
            comment.is_favorite = comment.favorite_by.filter(id=request.user.id).exists()

        # Serializar los comentarios y respuestas
        comment_serializer = CommentTreeSerializer(user_comments, many=True, context={'request': request})

        # Devolver los comentarios y respuestas en la respuesta
        return Response({
            'user_comments': comment_serializer.data,
        })



class SubmitAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Usar el serializer para validar y deserializar los datos
        create_serializer = SubmissionCreateSerializer(data=request.data)
        
        if create_serializer.is_valid():
            # Determinar el tipo de submission
            url = create_serializer.validated_data.get('url')
            submission_type = 'url' if url else 'ask'

            # Verificar si existe una submission con la misma URL
            if submission_type == 'url':
                existing_submission = Submission.objects.filter(url=url).first()
                if existing_submission:
                    # Responder con detalles si ya existe
                    response_serializer = SubmissionSerializer(existing_submission, context={'request': request})
                    return Response(
                        {"detail": "Submission already exists", "submission": response_serializer.data},
                        status=status.HTTP_200_OK
                    )

            # Crear y guardar la nueva submission
            new_submission = Submission(
                author=request.user,
                title=create_serializer.validated_data.get('title'),
                url=url,
                text=create_serializer.validated_data.get('text'),
                submission_type=submission_type
            )
            new_submission.save()

            # Usar el serializer detallado para la respuesta
            response_serializer = SubmissionSerializer(new_submission, context={'request': request})
            return Response(
                {"detail": "Submission created successfully", "submission": response_serializer.data},
                status=status.HTTP_201_CREATED
            )

        # Manejar errores de validación
        return Response(
            {"detail": "Invalid data", "errors": create_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class SubmissionDetailAPIView(APIView):

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'POST']:
            return [IsAuthenticated()]  # Requiere autenticación
        return [AllowAny()]  # Permite acceso público al método GET

    def get(self, request, pk):
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Filtrar comentarios principales (sin padre)
        comments = submission.comments.filter(parent__isnull=True)

        # Agregar datos adicionales al objeto Submission
        submission.shortened_url = get_shortened_url(submission.url) if submission.url else ""
        submission.time_ago = get_time_ago(submission.created_at)
        submission.num_comments = get_num_comments(submission)
        submission.has_voted = (
            submission.voted_by.filter(id=request.user.id).exists()
            if request.user.is_authenticated
            else False
        )
        submission.is_favorite = (
            submission.favorite_by.filter(id=request.user.id).exists()
            if request.user.is_authenticated
            else False
        )

        # Serializar el objeto Submission
        submission_serializer = SubmissionDetailSerializer(submission, context={'request': request})
        comments_serializer = CommentTreeSerializer(comments, many=True, context={'request': request})

        # Devolver la respuesta
        return Response({
            "submission": submission_serializer.data,
            "comments": comments_serializer.data,
        }, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar que el usuario autenticado es el autor de la submission
        if submission.author != request.user:
            raise PermissionDenied("You do not have permission to delete this submission.")

        # Eliminar la submission
        submission.delete()
        
        # Responder con un mensaje de éxito
        return Response({"detail": "Submission deleted successfully."}, status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar que el usuario autenticado es el autor de la submission
        if submission.author != request.user:
            raise PermissionDenied("You do not have permission to edit this submission.")

        # Usar el serializer de actualización para validar y deserializar los datos
        update_serializer = SubmissionUpdateSerializer(submission, data=request.data)

        if update_serializer.is_valid():
            # Guardar los cambios (sin afectar la URL)
            update_serializer.save()

            # Usar el serializer detallado para la respuesta
            response_serializer = SubmissionDetailSerializer(submission, context={'request': request})
            return Response(
                {"detail": "Submission updated successfully", "submission": response_serializer.data},
                status=status.HTTP_200_OK
            )

        # Manejar errores de validación
        return Response(
            {"detail": "Invalid data", "errors": update_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)
     

    def post(self, request, pk):
        
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar si el usuario autenticado es el autor de la submission
        if submission.author == request.user:
            return Response(
                {"detail": "You cannot comment on your own submission."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Asegurar que los comentarios sean siempre "padres"
        data = request.data.copy()  # Hacer una copia mutable de los datos de la solicitud
        data['parent'] = None  # Forzar que el campo 'parent' sea None

        # Usar el serializador para crear el comentario
        comment_serializer = CommentCreateSerializer(data=data, context={'request': request, 'submission': submission})


        if comment_serializer.is_valid():
            # Guardar el nuevo comentario
            comment_serializer.save()

            # Obtener todos los comentarios actualizados (incluyendo respuestas)
            comments = submission.comments.filter(parent__isnull=True)

            # Serializar la submission nuevamente con los comentarios actualizados
            submission_serializer = SubmissionDetailSerializer(submission, context={'request': request})
            comments_serializer = CommentTreeSerializer(comments, many=True, context={'request': request})

            # Devolver toda la información actualizada
            return Response({
                "submission": submission_serializer.data,
                "comments": comments_serializer.data,
                "detail": "Comment added successfully."
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "detail": "Invalid data",
            "errors": comment_serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class SubmissionVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden votar

    def post(self, request, pk):
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar si el usuario autenticado es el autor de la submission
        if submission.author == request.user:
            raise ValidationError({"detail": "You cannot vote on your own submission."})

        # Comprobar si el usuario ya ha votado
        if submission.voted_by.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You have already voted on this submission."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Añadir el voto (upvote)
        submission.voted_by.add(request.user)
        submission.points += 1  # Sumar 1 punto
        submission.save()  # Guardar los cambios

        # Serializar la submission actualizada
        serializer = SubmissionDetailSerializer(submission, context={'request': request})

        # Responder con información sobre la acción realizada
        return Response(
            {"detail": "Submission upvoted successfully.", 
             "submission": serializer.data},
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar si el usuario autenticado es el autor de la submission
        if submission.author == request.user:
            raise ValidationError({"detail": "You cannot remove a vote from your own submission."})

        # Comprobar si el usuario ha votado
        if not submission.voted_by.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You have not voted on this submission."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Eliminar el voto (downvote)
        submission.voted_by.remove(request.user)
        submission.points -= 1  # Restar 1 punto
        submission.save()  # Guardar los cambios

        # Serializar la submission actualizada
        serializer = SubmissionDetailSerializer(submission, context={'request': request})

        # Responder con información sobre la acción realizada
        return Response(
            {"detail": "Submission downvoted successfully.", 
             "submission": serializer.data},
            status=status.HTTP_200_OK
        )
    
class SubmissionFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden marcar favoritos

    def post(self, request, pk):
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar si el usuario ya ha marcado como favorito
        if request.user in submission.favorite_by.all():
            return Response(
                {"detail": "Submission is already in favorites."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Agregar a favoritos
        submission.favorite_by.add(request.user)

        # Obtener todas las submissions favoritas del usuario
        favorite_submissions = Submission.objects.filter(favorite_by=request.user)

        # Serializar las submissions favoritas
        serializer = SubmissionSerializer(favorite_submissions, many=True, context={'request': request})

        # Responder con la información
        return Response(
            {
                "detail": "Submission added to favorites successfully.",
                "favorite_submissions": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        # Obtener el objeto Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar si el usuario tiene la submission marcada como favorito
        if request.user not in submission.favorite_by.all():
            return Response(
                {"detail": "Submission is not in favorites."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Eliminar de favoritos
        submission.favorite_by.remove(request.user)

        # Obtener todas las submissions favoritas del usuario
        favorite_submissions = Submission.objects.filter(favorite_by=request.user)

        # Serializar las submissions favoritas
        serializer = SubmissionSerializer(favorite_submissions, many=True, context={'request': request})

        # Responder con la información
        return Response(
            {
                "detail": "Submission removed from favorites successfully.",
                "favorite_submissions": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class ToggleHideSubmissionAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def post(self, request, pk):
        # Obtener la Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar si la submission ya está oculta por el usuario
        if request.user in submission.hidden_by.all():
            return Response(
                {"detail": "You have already hidden this submission."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ocultar la submission
        submission.hidden_by.add(request.user)
        submission.save()  # Guardar los cambios
        action = "hidden"

        # Obtener todas las submissions que no están ocultas por el usuario
        visible_submissions = Submission.objects.exclude(hidden_by=request.user)

        # Serializar las submissions visibles
        serializer = SubmissionSerializer(visible_submissions, many=True)

        # Responder con el estado actualizado y las submissions visibles
        return Response(
            {
                "status": action,
                "visible_submissions": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        # Obtener la Submission
        submission = get_object_or_404(Submission, pk=pk)

        # Verificar si la submission está oculta por el usuario
        if request.user not in submission.hidden_by.all():
            return Response(
                {"detail": "You have not hidden this submission."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Dejar de ocultar la submission
        submission.hidden_by.remove(request.user)
        submission.save()  # Guardar los cambios
        action = "unhidden"

        # Obtener todas las submissions que no están ocultas por el usuario
        visible_submissions = Submission.objects.exclude(hidden_by=request.user)

        # Serializar las submissions visibles
        serializer = SubmissionSerializer(visible_submissions, many=True)

        # Responder con el estado actualizado y las submissions visibles
        return Response(
            {
                "status": action,
                "visible_submissions": serializer.data,
            },
            status=status.HTTP_200_OK
        )
