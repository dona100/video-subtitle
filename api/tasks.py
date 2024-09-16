
import os
import subprocess
from celery import shared_task
from django.conf import settings
from .models import Video, Subtitle
from .utils import parse_srt_file, save_subtitles_to_db  # Utility functions

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    
    # Define the output path for subtitles, storing it in MEDIA_ROOT/subtitles/{video_id}.srt
    output_path = os.path.join(settings.MEDIA_ROOT, f"subtitles/{video.id}.srt")
    
    # Ensure the 'subtitles' directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Extract subtitles using ffmpeg
    command = f"ffmpeg -i {video.video_file.path} -map 0:s:0 {output_path}"
    subprocess.call(command, shell=True)
    
    # Parse the extracted .srt file
    subtitles_content = parse_srt_file(output_path)
    
    # Save the subtitles to the database
    save_subtitles_to_db(video, subtitles_content)

