import re
from .models import Subtitle

def parse_srt_file(file_path):
    subtitles = []
    with open(file_path, 'r') as file:
        content = file.read()
        subtitle_entries = content.split("\n\n")
        for entry in subtitle_entries:
            lines = entry.split('\n')
            if len(lines) >= 3:
                timestamp = parse_timestamp(lines[1])
                subtitle_text = " ".join(lines[2:])
                subtitles.append({
                    'timestamp': timestamp,
                    'content': subtitle_text
                })
    return subtitles

def parse_timestamp(timestamp_str):
    pattern = r"(\d+):(\d+):(\d+),(\d+)"
    match = re.match(pattern, timestamp_str)
    if match:
        hours, minutes, seconds, milliseconds = map(int, match.groups())
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        return total_seconds
    return 0

def save_subtitles_to_db(video, subtitles_content):
    for subtitle in subtitles_content:
        Subtitle.objects.create(
            video=video,
            content=subtitle['content'],
            timestamp=subtitle['timestamp']
        )
