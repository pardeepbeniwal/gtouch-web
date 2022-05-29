from dataclasses import dataclass
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from video.models import Category, Video, FavoritVideo, UserHistory
from video.api.serializers import CategorySerializer, HomePageSerializer, VideoSerializer, FavoritVideoSerializer
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
from video.utils import time_to_second

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


class HomeApiView(APIView):
    category_data = None

    def get_category(self):
        queryset = Category.objects.all()
        self.category_data = CategorySerializer(queryset,many=True).data
        return self.category_data

    def get_video_by_category(self, cat_id):
        data = []
        records = Video.objects.filter(category=cat_id).order_by("-id")
        for rec in records:
            inner = {}
            duration = rec.duration
            inner['name'] = rec.title
            inner['duration'] = int(duration)
            inner['ispremium'] = 0
            inner['entryid'] = str(rec.id)
            inner['channel_small_image_url'] = settings.STATIC_PATH_URL+str(rec.thumbnail)
            inner['thumburl'] = {"h_thumburl":settings.STATIC_PATH_URL+str(rec.thumbnail),"v_thumburl": None}
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
            inner['imgurl'] = settings.STATIC_PATH_URL+str(rec.thumbnail)
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
    
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not FavoritVideo.objects.filter(user=request.user.id, video=request.data['video']):
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if FavoritVideo.objects.filter(user=request.user.id,id=instance.id):
                self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
