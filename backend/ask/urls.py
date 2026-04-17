from django.urls import path
from . import views

urlpatterns = [
    path("", views.ask, name="ask"),
    path('vote/<int:submission_id>/', views.vote_submission_ask, name='vote_submission_ask'),
]
