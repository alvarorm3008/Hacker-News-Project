import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    DEFAULT_PROFILE_IMAGE = "https://aswimagenesfinal.s3.amazonaws.com/default.jpg"
    DEFAULT_BANNER_IMAGE = "https://aswimagenesfinal.s3.amazonaws.com/defaultbanner.png"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    karma = models.IntegerField(default=1)
    api_key = models.CharField(max_length=255, blank=False, null=False, default="default-api-key")
    imagen_perfil_url = models.URLField(max_length=500, null=True, blank=True)
    banner_perfil_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    @property
    def get_imagen_perfil(self):
        """Retorna la URL de la imagen de perfil o la imagen por defecto si no existe"""
        if not self.imagen_perfil_url:
            return self.DEFAULT_PROFILE_IMAGE
        
        # Verificar si la imagen existe en S3
        try:
            import boto3
            from django.conf import settings
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=settings.AWS_SESSION_TOKEN,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            # Extraer el nombre del archivo de la URL
            path = self.imagen_perfil_url.split(settings.AWS_S3_CUSTOM_DOMAIN + '/')[-1]
            
            # Verificar si el objeto existe
            s3_client.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=path)
            return self.imagen_perfil_url
        except:
            # Si hay cualquier error, devolver la imagen por defecto
            self.imagen_perfil_url = self.DEFAULT_PROFILE_IMAGE
            self.save()
            return self.DEFAULT_PROFILE_IMAGE
        
    @property
    def get_banner_perfil(self):
        """Retorna la URL del banner o la imagen por defecto si no existe"""
        if not self.banner_perfil_url:
            return self.DEFAULT_BANNER_IMAGE
        
        try:
            import boto3
            from django.conf import settings
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=settings.AWS_SESSION_TOKEN,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            path = self.banner_perfil_url.split(settings.AWS_S3_CUSTOM_DOMAIN + '/')[-1]
            s3_client.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=path)
            return self.banner_perfil_url
        except:
            self.banner_perfil_url = self.DEFAULT_BANNER_IMAGE
            self.save()
            return self.DEFAULT_BANNER_IMAGE
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()