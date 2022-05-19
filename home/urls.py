from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name='home'),
    path("login", views.login, name='login'),
    path("register", views.register, name='register'),
    path("video_feed", views.video_feed, name='video_feed'),
    # path("user", views.usersuc, name='user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
