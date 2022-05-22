from rest_framework.routers import DefaultRouter

from video.api import views

router = DefaultRouter()


router.register(r"category", viewset=views.CategoryReadOnlyViewSet)
router.register(r"video_list", viewset=views.VideoReadOnlyViewSet)
urlpatterns = []
urlpatterns += router.urls