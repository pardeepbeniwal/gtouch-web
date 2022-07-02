from rest_framework.routers import DefaultRouter
from django.urls import path
from video.api import views

router = DefaultRouter()


router.register(r"category", viewset=views.CategoryReadOnlyViewSet)
router.register(r"video_list", viewset=views.VideoReadOnlyViewSet)
router.register(r"favorite", viewset=views.FavoritVideoViewSet)
router.register(r"watched_video", viewset=views.WatchVideoViewSet)
router.register(r"live", viewset=views.LiveViewSet)
#router.register(r"category_by_video", viewset=views.VideByCategoryView)
urlpatterns = [
    path('home', views.HomeApiView.as_view(), name='home'),
    path('category_by_video/<int:id>', views.CategoryByVideoView.as_view(), name='category_by_video')
]


urlpatterns += router.urls