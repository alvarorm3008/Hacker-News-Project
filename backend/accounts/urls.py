from django.urls import path

from comments.views import vote_comment
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
   
    path('hidden_submissions/', views.hidden_submissions, name='hidden_submissions'), 
    path('hidden_submissions/unhide/<int:submission_id>/', views.unhide_submission, name='unhide_submission'),
    path('voted/', views.voted_submissions, name='voted_submissions'),
    path('votedcomms/', views.voted_comments, name='voted_comments'),
    path('unvote/<int:submission_id>/', views.unvote_submission, name='unvote_submission'),
    path('unvotecomms/<int:comment_id>/', views.unvote_comment, name='unvote_comment'),
    path('favorite_submissions/', views.favorite_submissions, name='favorite_submissions'),
    path('accounts/user/<str:username>/favorite-comments/', views.favorite_comments, name='favorite_comments'),
    path('accounts/user/<str:username>/favorite-submissions/', views.favorite_submissions, name='favorite_submissions'),

    path('submission/<int:submission_id>/unfavorite/', views.unfavorite_submission, name='unfavorite_submission'),
    path('comment/<int:comment_id>/unfavorite/', views.unfavorite_comment, name='unfavorite_comment'),
    path('complete_signup/', views.complete_signup, name='complete_signup'),

    path('profile/<str:username>/', views.author_profile, name='author_profile'),
    path('profile/<str:username>/submissions/', views.author_submissions, name='author_submissions'),
    path('profile/<str:username>/comments/', views.author_comments, name='author_comments'),

    path('vote/<int:comment_id>/', vote_comment, name='vote_comment'),



]