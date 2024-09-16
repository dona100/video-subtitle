from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Video,Subtitle
from .tasks import process_video

class VideoUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        video_file = request.data['video_file']
        video = Video.objects.create(video_file=video_file)
        process_video.delay(video.id)  # Run video processing in the background
        return Response({"message": "Video uploaded and processing started."})



class SubtitleSearchView(APIView):
    def get(self, request, phrase, video_id):
        subtitles = Subtitle.objects.filter(
            video_id=video_id,
            content__icontains=phrase
        )
        return Response([{'timestamp': subtitle.timestamp, 'content': subtitle.content} for subtitle in subtitles])

