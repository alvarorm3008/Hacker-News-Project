from django.urls import path
from .views import all_comments, delete_comment, edit_comment, comment_detail, vote_comment, favorite_comment, reply_comment

urlpatterns = [
    path("", all_comments, name='comments'),
    path('comment/<int:pk>/', comment_detail, name='comment_detail'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    path('comment/<int:pk>/edit', edit_comment, name='edit_comment'),
    path('vote/<int:comment_id>/', vote_comment, name='vote_comment'),
    path('favorite/<int:comment_id>/', favorite_comment, name='favorite_comment'), 
    path('reply/<int:pk>/', reply_comment, name='reply_comment'), 
]
