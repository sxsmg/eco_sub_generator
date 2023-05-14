from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VideoForm
from .models import Video, Subtitle
from celery import shared_task
from .tasks import extract_subtitles

import os
from mongoengine import connect


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            # Trigger the video processing task
            process_video.delay(str(video.id))
            # Additional logic or processing
        return redirect('ecowiser:video_detail', pk=video.pk)  # Redirect to video detail view
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})


@shared_task
def process_video(video_id):
    # Get the video object
    video = get_object_or_404(Video, id=video_id)

    # Process the uploaded video and get the video path
    video_path = video.video_file.path

    # Trigger the subtitle extraction task
    result = extract_subtitles.delay(video_path)
    # Optionally handle the task result or return a response
    task_id = result.id
    response_data = {
        'task_id': task_id
    }
    return response_data


def search_subtitles(request):
    search_text = request.GET.get('search_text')

    # Create a query to search for subtitles based on text
    query = Subtitle.objects(subtitle_text=search_text)
    #print(query)
    # Process the query results and extract relevant data
    subtitles = list(query)

    # Pass the search results to the template or return as JSON response
    return render(request, 'search_results.html', {'subtitles': subtitles})


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    # Additional logic or processing related to video detail
    return render(request, 'video_detail.html', {'video': video})
