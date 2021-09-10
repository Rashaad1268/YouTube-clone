from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_page, name="home"),
    path('upload/', views.video_upload_view, name="upload"),
    path('watch/<int:video_id>/<str:video_title>/', views.video_watch_view, name="watch"),
    path('delete/<int:video_id>/<str:video_title>/', views.video_delete_view, name="delete"),
    path('edit/<int:video_id>/<str:video_title>/', views.video_edit_view, name="edit"),
    path('private/videos/', views.private_videos, name="private"),
    path('channel/<int:channel_id>/', views.channel_view, name="channel"),
    path('delete-comment/<int:comment_id>/', views.comment_delete_view, name="delete_comment"),
    path('contact/', views.contact_view, name ="contact"),
    path('subscribe/', views.subscribe_view, name ="subscribe"),
    path('like/', views.like_view, name ="like"),
]
