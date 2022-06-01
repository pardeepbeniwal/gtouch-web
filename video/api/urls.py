from rest_framework.routers import DefaultRouter
from django.urls import path
from video.api import views

router = DefaultRouter()


router.register(r"category", viewset=views.CategoryReadOnlyViewSet)
router.register(r"video_list", viewset=views.VideoReadOnlyViewSet)
router.register(r"favorite", viewset=views.FavoritVideoViewSet)
router.register(r"live", viewset=views.LiveViewSet)
urlpatterns = [
    path('home', views.HomeApiView.as_view(), name='home')
]


urlpatterns += router.urls