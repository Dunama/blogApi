from django.urls import path

from . import web_views

urlpatterns = [
    path('', web_views.index, name='home'),
    # Add both with and without trailing slashes because the templates use mixed styles.
    path('signin', web_views.signin, name='signin_noslash'),
    path('signin/', web_views.signin, name='signin'),
    path('signup', web_views.signup, name='signup_noslash'),
    path('signup/', web_views.signup, name='signup'),
    path('upload', web_views.upload, name='upload_noslash'),
    path('upload/', web_views.upload, name='upload'),
    path('settings', web_views.settings_view, name='settings_noslash'),
    path('settings/', web_views.settings_view, name='settings'),
    path('search', web_views.search, name='search_noslash'),
    path('search/', web_views.search, name='search'),
    path('profile', web_views.profile, name='profile_noslash'),
    path('profile/', web_views.profile, name='profile'),
    path('profile/<str:username>/', web_views.profile, name='profile_detail'),
    path('like-post', web_views.like_post, name='like_post_noslash'),
    path('like-post/', web_views.like_post, name='like_post'),
    path('comment-post', web_views.comment_post, name='comment_post_noslash'),
    path('comment-post/', web_views.comment_post, name='comment_post'),
    path('follow', web_views.follow, name='follow_noslash'),
    path('follow/', web_views.follow, name='follow'),
    path('delete-post', web_views.delete_post, name='delete_post_noslash'),
    path('delete-post/', web_views.delete_post, name='delete_post'),
    path('logout', web_views.logout_view, name='logout_noslash'),
    path('logout/', web_views.logout_view, name='logout'),
]
