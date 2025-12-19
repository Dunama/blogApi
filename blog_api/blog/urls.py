"""
URL configuration for blog_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', include('accounts.web_urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('comments.urls')),
    path('admin/', admin.site.urls),
]

# Serve media files - enabled by DEBUG or DJANGO_SERVE_MEDIA env var
_serve_media = settings.DEBUG or os.environ.get('DJANGO_SERVE_MEDIA', '').lower() in ('1', 'true', 'yes', 'on')
if _serve_media:
    # Use re_path for more robust media serving that works in production
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
