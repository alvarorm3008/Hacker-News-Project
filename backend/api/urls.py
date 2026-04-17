
from django.urls import path
from . import views

urlpatterns = [
    path('hidden_submissions', views.HiddenSubmissionsApi.as_view(), name = 'profile_hidden_submissions_api'),
    path('voted_submissions', views.VotedSubmissionsAPI.as_view(), name='voted_submissions_api'),
    path('voted_comments', views.VotedCommentsAPI.as_view(), name='voted_comments_api'),
    path('favorite_submissions', views.FavoriteSubmissionsAPI.as_view(), name='favorite_submissions_api'),
    path('favorite_comments', views.FavoriteCommentsAPI.as_view(), name='favorite_comments_api'),
    path('author/<str:username>/submissions', views.AuthorSubmissionsAPI.as_view(), name='author_submissions_api'),
    path('author/<str:username>/comments', views.AuthorCommentsAPI.as_view(), name='author_comments_api'),
    path('author/<str:username>/profile', views.AuthorProfileAPI.as_view(), name='author_profile_api'),
    path('author/<str:username>/favorite_submissions', views.AuthorFavoriteSubmissionsAPI.as_view(), name='author_favorite_submissions_api'),
    path('author/<str:username>/favorite_comments', views.AuthorFavoriteCommentsAPI.as_view(), name='author_favorite_comments_api'), 
    path('profile', views.ProfileDetailAPI.as_view(), name='profile_detail_api'),
    path('profile/media/<str:media_type>', views.DeleteProfileMediaAPI.as_view(), name='delete-profile-media'),
    path('comments', views.CommentsAPI.as_view(), name='comments_api'),
    path('comments/<int:pk>', views.CommentDetailAPI.as_view(), name='comment_detail_api'),
    path('comments/<int:pk>/reply', views.ReplyCommentAPI.as_view(), name='reply_comment_api'),
    path('comments/<int:pk>/edit', views.EditCommentAPI.as_view(), name='edit_comment_api'),
    path('comments/<int:comment_id>/vote', views.VoteCommentAPI.as_view(), name='vote_comment_api'),
    path('comments/<int:comment_id>/favorite', views.FavoriteCommentAPI.as_view(), name='favorite_comment_api'),
    path('news', views.NewsApi.as_view(), name = 'news_api'),
    path('ask', views.AskAPI.as_view(), name = 'ask_api'),
    path('newest', views.NewestAPI.as_view(), name = 'newest_api'),
    path('submit', views.SubmitAPIView.as_view(), name='api_submit_submission'),
    path('submission/<int:pk>', views.SubmissionDetailAPIView.as_view(), name='api_submission_detail'),
    path('submission/<int:pk>/vote', views.SubmissionVoteAPIView.as_view(), name='api_vote_submission'),
    path('submission/<int:pk>/favorite', views.SubmissionFavoriteAPIView.as_view(), name='api_favorite_submission'),
    path('submission/<int:pk>/hide', views.ToggleHideSubmissionAPIView.as_view(), name='api_hide_submission'),
    path('threads', views.ThreadsAPIView.as_view(), name='api_threads'),
    path('author/<str:username>/voted_submissions', views.VotedSubmissionsAPI.as_view(), name='author_voted_submissions_api'),

]