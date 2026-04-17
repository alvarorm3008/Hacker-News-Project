from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_submission, name='submit_submission'),
    path('submission/<int:pk>/', views.submission_detail, name='submission_detail'),  # URL para la vista de detalle de la submission
    path('submission/<int:pk>/edit/', views.edit_submission, name='edit_submission'),
    path('submission/<int:pk>/delete/', views.delete_submission, name='delete_submission'),
    path('hide/<int:submission_id>/', views.hide_submission, name='hide_submission'),
    path('favorite/<int:submission_id>/', views.favorite_submission, name='favorite_submission'),
]
