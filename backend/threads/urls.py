from django.urls import path
from .views import threads
from . import views

urlpatterns = [
    path("", views.user_comments, name='threads'),
]
