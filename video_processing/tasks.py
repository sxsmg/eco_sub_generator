from celery_script import app
from subprocess import Popen, PIPE
from .models import Subtitle

import os
from mongoengine import connect

@app.task
def extract_subtitles(video_path):
    # Disconnect existing MongoDB connection
    ###connect(alias='default', disconnect=True)
    
    # Establish a new MongoDB connection
    ###connect(host=MONGODB_CONNECTION_STRING)
    # Run ccextractor as a subprocess to extract subtitles
    command = ['ccextractor', video_path]
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    # Parse the extracted subtitles
    subtitles = parse_subtitles(stdout)

    # Store the subtitles in MongoDB
    store_subtitles(subtitles)

    # Optionally return or handle the extracted subtitles
    return subtitles


def parse_subtitles(subtitle_data):
    # Implement your parsing logic here
    # Parse the subtitle_data and extract relevant information
    # Return the parsed subtitles
    subtitles = []
    # Example parsing logic:
    for line in subtitle_data.decode('utf-8').split('\n'):
        if line.strip():
            subtitle_text = line.strip()
            start_time, end_time = parse_subtitle_time(line)
            subtitles.append(Subtitle(subtitle_text=subtitle_text, start_time=start_time, end_time=end_time))
    return subtitles


def parse_subtitle_time(subtitle_line):
    # Implement your time parsing logic here
    # Parse the subtitle_line and extract start_time and end_time
    start_time = 0.0
    end_time = 0.0
    # Example time parsing logic:
    start_time_str, end_time_str = subtitle_line.split(' --> ')
    start_time_parts = start_time_str.split(':')
    end_time_parts = end_time_str.split(':')
    start_time = float(start_time_parts[0]) * 3600 + float(start_time_parts[1]) * 60 + float(start_time_parts[2].replace(',', '.'))
    end_time = float(end_time_parts[0]) * 3600 + float(end_time_parts[1]) * 60 + float(end_time_parts[2].replace(',', '.'))
    return start_time, end_time


def store_subtitles(subtitles):
    # Store the subtitles in MongoDB using mongoengine
    Subtitle.objects.insert(subtitles)
