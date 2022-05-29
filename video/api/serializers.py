from rest_framework import serializers
from video.models import Category, Video, FavoritVideo, UserHistory
from django.conf import settings

class CategorySerializer(serializers.ModelSerializer):
    cat_name = serializers.SerializerMethodField()
    catagory_id = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("cat_name", "catagory_id")
    
    def get_cat_name(self,obj):
        return obj.name
    
    def get_catagory_id(self,obj):
        return obj.id

class VideoSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    category_id = serializers.IntegerField(source='category.id')
    thubmbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id','title','description','created_at','video_file','duration','category','category_id','thubmbnail',)

    def get_thubmbnail(self, obj):
        if obj.thumbnail:
            return settings.STATIC_URL_TEMP+obj.thumbnail


class FavoritVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritVideo
        fields = ("id", "video", "user","created_at")



class HomePageSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    category_id = serializers.IntegerField(source='category.id')
    thubmbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id','title','description','created_at','video_file','duration','category','category_id','thubmbnail',)

    def get_thubmbnail(self, obj):
        if obj.thumbnail:
            return settings.STATIC_URL_TEMP+obj.thumbnail