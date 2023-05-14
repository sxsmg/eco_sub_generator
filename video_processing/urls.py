from django.urls import path
from .views import upload_video, search_subtitles, video_detail

app_name = 'ecowiser'

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('search/', search_subtitles, name='search_subtitles'),
    path('video_detail/<int:pk>/', video_detail, name='video_detail'),
]