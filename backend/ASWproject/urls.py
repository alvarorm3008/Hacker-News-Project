"""
URL configuration for ASWproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation for Hacker News",
        default_version='v1',
        description="API documentation for the project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # Sin autenticación para Swagger
)


urlpatterns = [
    path('', include('news.urls')),  # Ruta principal (Home)
    path('news/', include('news.urls')),  # Noticias
    path('newest/', include('newest.urls')),  # publicaciones ordenadas
    path('threads/', include('threads.urls')),  # threads
    path('comments/', include('comments.urls')),  # comments
    path('ask/', include('ask.urls')),  # ask
    path('submissions/', include('submissions.urls')),  # submit
    path('admin/', admin.site.urls),  # Admin 
    path('accounts/', include('accounts.urls')),  # Cuentas
    path('accounts/', include('allauth.urls')),
    path('', include('news.urls')),  # Asegúrate de que esta línea apunte a tu aplicación principal
    path('api/', include('api.urls')),  # API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

