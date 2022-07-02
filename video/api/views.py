from dataclasses import dataclass
from multiprocessing import context
from unicodedata import category
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from video.models import Category, Video, FavoritVideo, UserHistory, Live
from video.api.serializers import CategorySerializer, HomePageSerializer, VideoDetailSerializer, VideoSerializer, FavoritVideoSerializer, LiveSerializer, WatchVideoSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from video.api.filters import VideoFilter
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework import generics, mixins, views
from rest_framework.views import APIView
from django.conf import settings
from django.db.models import Q
from video.utils import time_to_second
cloud_front_url = settings.CLOUD_FRONT_URL



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1500


class CategoryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    search_fields = ['name']


class VideoReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    filter_class = VideoFilter
    filter_fields = ('id','title','description','cast_details')
    search_fields = ('id','title','description','cast_details')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = VideoDetailSerializer(instance, context = {
                            'request': request
                        })
        return Response(serializer.data)


class HomeApiView(APIView):
    category_data = None

    def get_category(self):
        queryset = Category.objects.all()
        self.category_data = CategorySerializer(queryset,many=True).data
        return self.category_data

    def get_video_by_category(self, cat_id):
        data = []
        records = Video.objects.filter(category=cat_id, status=1).order_by("-id")
        for rec in records:
            inner = {}
            duration = rec.duration
            inner['name'] = rec.title
            inner['duration'] = int(duration)
            inner['ispremium'] = 0
            inner['entryid'] = str(rec.id)
            inner['channel_small_image_url'] = cloud_front_url+str(rec.v_thumbnail.name)
            inner['thumburl'] = {"h_thumburl":cloud_front_url+str(rec.h_thumbnail.name),"v_thumburl": cloud_front_url+str(rec.v_thumbnail.name)}
            data.append(inner)
        return data
       

    def get_home_data(self):
        data = []
        for cat in self.category_data:
            inner = {
                "cat_type": "cat",
                "title_tag_name": cat.get("cat_name"),
                "image_type": "h",
                "categoryid": cat.get("catagory_id")
            }
            inner["search_tag"] = self.get_video_by_category(cat.get("catagory_id"))
            data.append(inner)
        return  data
    
    def get_carousel_data(self):
        data = []
        records = Video.objects.filter(section__name='Carousel').order_by("-id")
        for rec in records:
            inner = {}
            inner['entryid'] = str(rec.id)
            inner['imgurl'] = cloud_front_url+str(rec.v_thumbnail.name)
            inner['priority'] = 1
            data.append(inner)

        return data

    def get(self, request, format=None):
        data = {}
        data['header'] = self.get_category()
        data['home'] = self.get_home_data()
        data['Carousel'] = self.get_carousel_data()
        data['continue_watching'] = []
        return Response(data, status=status.HTTP_200_OK)


class FavoritVideoViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = FavoritVideoSerializer
    queryset = FavoritVideo.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoritVideo.objects.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        fav_list = list(FavoritVideo.objects.filter(user=self.request.user.id).values_list('video', flat=True))
        vd_list = Video.objects.filter(id__in=fav_list)
        if vd_list:
            return Response({"Favourite": VideoSerializer(vd_list,many=True).data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "There is no video in your favorite list"}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        
        try:
            entryid = request.data['entryid']
            if not Video.objects.filter(id=entryid).count():
                return Response({"message":"Provided entryid does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message":"entryid is required."}, status=status.HTTP_400_BAD_REQUEST)
        request.data['video'] = request.data['entryid']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not FavoritVideo.objects.filter(user=request.user.id, video=entryid):
            self.perform_create(serializer)
            return Response({"message": "Successfully added in favourite list"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Already added in favourite list"}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            video_id = kwargs.get('pk')
            video = FavoritVideo.objects.filter(user=request.user.id,video=video_id)
            if video:
                video.delete()
            else:
                return Response({"message": "Video is not added in your favourite list"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Something went wrong!!","error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Deleted Successfully"},status=status.HTTP_200_OK)

class LiveViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LiveSerializer
    queryset = Live.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    search_fields = ['title']

class CategoryByVideoView(APIView):
    category_data = None

    def get_category(self):
        queryset = Category.objects.all()
        self.category_data = CategorySerializer(queryset,many=True).data
        return self.category_data

    def get(self, request, id):
        try:
            Category.objects.get(id=id)
            vid_list = Video.objects.filter(category_id=id)
            data = VideoSerializer(vid_list, many=True).data
            return Response({"Video":data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e),"message":"Category not found"}, status=status.HTTP_200_OK)


class WatchVideoViewSet(mixins.CreateModelMixin,                   
                   mixins.UpdateModelMixin,                   
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = WatchVideoSerializer
    queryset = UserHistory.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserHistory.objects.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        fav_list = list(UserHistory.objects.filter(user=self.request.user.id).values_list('video', flat=True))
        vd_list = Video.objects.filter(id__in=fav_list)
        if vd_list:
            return Response({"watched_video": VideoSerializer(vd_list,many=True).data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "There is no video in your favorite list"}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        if not request.data.get('watch_duration_time'):
            return Response({"message":"watch_duration_time is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            entryid = request.data['entryid']
            if not Video.objects.filter(id=entryid).count():
                return Response({"message":"Provided entryid does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message":"entryid is required."}, status=status.HTTP_400_BAD_REQUEST)
        request.data['video'] = request.data['entryid']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        history = UserHistory.objects.filter(user=request.user.id, video=entryid)
        if not history:
            self.perform_create(serializer)
            return Response({"message": "Successfully added in watch list"}, status=status.HTTP_201_CREATED)
        else:
            history.update(watch_duration_time=request.data.get('watch_duration_time'))
            return Response({"message": "Watch duration time is updated"}, status=status.HTTP_200_OK)