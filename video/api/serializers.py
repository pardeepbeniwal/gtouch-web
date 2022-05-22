from rest_framework import serializers
from video.models import Category, VideoModel
from django.conf import settings

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "id")

class VideoSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    category_id = serializers.IntegerField(source='category.id')
    thubmbnail = serializers.SerializerMethodField()

    class Meta:
        model = VideoModel
        fields = ('id','title','description','created_at','video_file','duration','category','category_id','thubmbnail',)

    def get_thubmbnail(self, obj):
        if obj.thumbnail:
            return settings.STATIC_URL_TEMP+obj.thumbnail