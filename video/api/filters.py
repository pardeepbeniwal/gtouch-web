import django_filters
from video.models import VideoModel


class VideoFilter(django_filters.FilterSet):

    class Meta:
        model = VideoModel
        fields = ['category', 'title', 'description']