from rest_framework import serializers
from accounts.models import Profile
from ASWproject.utils import calculate_karma

class ProfileSerializer(serializers.ModelSerializer):
    karma = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['about', 'imagen_perfil_url', 'banner_perfil_url', 'api_key', 'karma', 'created_at']

    def get_karma(self, obj):
        return calculate_karma(obj.user)

    def get_created_at(self, obj):
        return obj.user.date_joined