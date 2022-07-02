from fileinput import filename
from rest_framework import serializers
from video.models import Category, Video, FavoritVideo, UserHistory,Live
from django.conf import settings
import os
CLOUD_FRONT = settings.CLOUD_FRONT_URL

def get_video(obj):
    filename = obj.video_file.name
    filename = filename.replace('video_files','m3u8_files')
    extension = os.path.splitext(filename)[1]
    filename = filename.replace(extension,'.m3u8')
    return CLOUD_FRONT+"{}".format(filename)

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

class VideoListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    category_id = serializers.IntegerField(source='category.id')
    name = serializers.SerializerMethodField()
    thubmbnail = serializers.SerializerMethodField()
    entryid = serializers.SerializerMethodField()
    video_file= serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('entryid','name','description','cast_details','created_at','video_file','duration','category','category_id','thubmbnail')

    def get_entryid(self, obj):
        return obj.id
    
    def get_name(self, obj):
        return obj.title

    def get_thubmbnail(self, obj):
        if obj.v_thumbnail:
            return CLOUD_FRONT+obj.v_thumbnail.name
    
    def get_video_file(self,obj):
         return get_video(obj)

class VideoDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    category_id = serializers.IntegerField(source='category.id')
    name = serializers.SerializerMethodField()
    thubmbnail = serializers.SerializerMethodField()
    entryid = serializers.SerializerMethodField()
    recommended = serializers.SerializerMethodField()
    video_file= serializers.SerializerMethodField()
    watch_duration_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = ('entryid','name','description','cast_details','created_at','video_file','duration','category','category_id','thubmbnail','recommended','watch_duration_time')

    def get_entryid(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.title

    def get_thubmbnail(self, obj):
        if obj.v_thumbnail:
            return CLOUD_FRONT+obj.v_thumbnail.name

    def get_recommended(self,obj):
        video_list = Video.objects.filter(category = obj.category).exclude(id=obj.id)
        return VideoListSerializer(video_list,many=True).data

    def get_video_file(self,obj):
       return get_video(obj)
    
    def get_watch_duration_time(self,obj):
        if self.context.get('request').user.id:
            history = UserHistory.objects.filter(video=obj,user=self.context.get('request').user.id).first()
            if history:
                return history.watch_duration_time
        return 0
        
    

class VideoSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    category_id = serializers.IntegerField(source='category.id')
    name = serializers.SerializerMethodField()
    thubmbnail = serializers.SerializerMethodField()
    entryid = serializers.SerializerMethodField()
    video_file= serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('entryid','name','description','cast_details','created_at','video_file','duration','category','category_id','thubmbnail')

    def get_entryid(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.title

    def get_thubmbnail(self, obj):
        if obj.v_thumbnail:
            return CLOUD_FRONT+obj.v_thumbnail.name

    def get_video_file(self,obj):
       return get_video(obj)


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
        if obj.v_thumbnail:
            return CLOUD_FRONT+obj.v_thumbnail.name

class LiveSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Live
        fields = ("id", "thumbnail", "url", "title")
    
    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return CLOUD_FRONT+obj.thumbnail.name

class WatchVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHistory
        fields = ("id", "video", "user","watch_duration_time", "created_at")