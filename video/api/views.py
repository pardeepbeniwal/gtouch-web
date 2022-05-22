from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from video.models import Category, VideoModel
from video.api.serializers import CategorySerializer, VideoSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from video.api.filters import VideoFilter


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
    queryset = VideoModel.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    filter_class = VideoFilter
    #filter_fields = ('title','description','category')