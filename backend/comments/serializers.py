from rest_framework import serializers
from .models import Comment
from ASWproject.utils import get_time_ago

class CommentSerializer(serializers.ModelSerializer):
     # Solo incluye el título de la submission
    submission_title = serializers.SerializerMethodField()
    submission_id = serializers.SerializerMethodField()  # Nuevo campo
    author = serializers.StringRelatedField()
    time_ago = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()
    parent_comment = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'points', 'author', 'submission_title', 'submission_id', 'time_ago', 'has_voted', 'is_favorite', 'parent_id', 'parent_comment']

    def get_submission_title(self, obj):
        return obj.submission.title  # Devuelve solo el título de la submission

    def get_submission_id(self, obj):
        return obj.submission.id  # Devuelve el ID de la submission
    
    def get_time_ago(self, obj):

        return get_time_ago(obj.created_at)

    def get_has_voted(self, obj):
        request = self.context.get('request')
        return obj.voted_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return obj.favorite_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False
    
    def get_parent_id(self, obj):
        # Devuelve el ID del comentario padre si existe, de lo contrario None
        return obj.parent.id if obj.parent else None
    
    def get_parent_comment(self, obj):
        return obj.parent.text if obj.parent else None
    
class CommentCreateSerializer(serializers.ModelSerializer):
    # Definimos solo el texto del comentario, ya que el autor y la submission se asignarán automáticamente
    class Meta:
        model = Comment
        fields = ['text']

    def create(self, validated_data):
        # Asignar el usuario autenticado y la submission al crear el comentario
        user = self.context['request'].user
        submission = self.context['submission']  # La submission se pasa a través del contexto

        comment = Comment.objects.create(
            author=user,
            submission=submission,
            **validated_data
        )
        return comment
    
class CommentTreeSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()
    submission_title = serializers.SerializerMethodField()
    submission_id = serializers.SerializerMethodField()  # Nuevo campo
    replies = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    parent_comment = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'points', 'time_ago', 'has_voted', 'is_favorite', 'submission_title', 'submission_id', 'parent_comment', 'replies']

    def get_time_ago(self, obj):
        return get_time_ago(obj.created_at)
    
    def get_submission_title(self, obj):
        return obj.submission.title  # Devuelve solo el título de la submission
    
    def get_submission_id(self, obj):
        return obj.submission.id  # Devuelve el ID de la submission
    
    def get_has_voted(self, obj):
        request = self.context.get('request')
        return obj.voted_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return obj.favorite_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False
    
    def get_replies(self, obj):
        # Serializar las respuestas recursivamente
        replies = obj.replies.all()
        return CommentTreeSerializer(replies, many=True, context=self.context).data
    
    def get_parent_comment(self, obj):
        return obj.parent.text if obj.parent else None
