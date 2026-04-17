from django.urls import path
from . import views

urlpatterns = [
    path("", views.news, name="news"),
    path('hide/<int:submission_id>/', views.news_hide_submission, name='news_hide_submission'),
    path('vote/<int:submission_id>/', views.vote_submission, name='vote_submission'),
]