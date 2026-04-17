from django.urls import path
from . import views

urlpatterns = [
    path("", views.newest, name="newest"),
    path('hide/<int:submission_id>/', views.newest_hide_submission, name='newest_hide_submission'),
    path('vote/<int:submission_id>/', views.vote_submission, name='vote_submission'),
]