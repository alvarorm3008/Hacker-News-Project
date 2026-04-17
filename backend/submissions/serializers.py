

from ASWproject.utils import get_num_comments, get_shortened_url, get_time_ago
from rest_framework import serializers
from submissions.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    shortened_url = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'id', 'title', 'url', 'author', 'points',
            'submission_type', 'time_ago', 'shortened_url', 
            'num_comments', 'has_voted', 'is_favorite'
        ]

    def get_time_ago(self, obj):
        return get_time_ago(obj.created_at)

    def get_shortened_url(self, obj):
        return get_shortened_url(obj.url)

    def get_num_comments(self, obj):
        return get_num_comments(obj)

    def get_has_voted(self, obj):
        request = self.context.get('request')
        return obj.voted_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return obj.favorite_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False

    def to_representation(self, instance):
            """Override to handle null URLs."""
            representation = super().to_representation(instance)
            if representation.get('url') is None:
                representation['url'] = ''  # Replace null with an empty string
            return representation
    
class SubmissionDetailSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    shortened_url = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'id', 'title', 'url', 'author', 'points',
            'submission_type', 'time_ago', 'shortened_url', 
            'num_comments', 'has_voted', 'text', 'is_favorite'
        ]

    def get_time_ago(self, obj):
        return get_time_ago(obj.created_at)

    def get_shortened_url(self, obj):
        return get_shortened_url(obj.url)

    def get_num_comments(self, obj):
        return get_num_comments(obj)

    def get_has_voted(self, obj):
        request = self.context.get('request')
        return obj.voted_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return obj.favorite_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False

class SubmissionCreateSerializer(serializers.ModelSerializer):
    url = serializers.URLField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Submission
        fields = ['title', 'url', 'text']

    def validate(self, data):
        # Asegurarse de que `url` sea una cadena vacía si es `null` o no proporcionado
        data['url'] = data.get('url') or ""

        # Validar que al menos uno de los campos `url` o `text` esté presente
        if not data['url'] and not data.get('text'):
            raise serializers.ValidationError("Debes proporcionar una URL o un texto.")
        return data

class SubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['title', 'text']  # Excluir el campo 'url'
 

    
class SubmissionAskSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            'id', 'title', 'author', 'points',
            'submission_type', 'time_ago', 
            'num_comments', 'has_voted', 'is_favorite'
        ]
        

    def get_time_ago(self, obj):
        return get_time_ago(obj.created_at)

    def get_num_comments(self, obj):
        return get_num_comments(obj)

    def get_has_voted(self, obj):
        request = self.context.get('request')
        return obj.voted_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False
    
    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return obj.favorite_by.filter(id=request.user.id).exists() if request and request.user.is_authenticated else False