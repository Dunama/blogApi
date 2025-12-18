from django.urls import path

from .views import MeView, SignUpView, TokenLoginView, TokenRefreshView


urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/login/', TokenLoginView, name='login'),
    path('auth/refresh/', TokenRefreshView, name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
]
