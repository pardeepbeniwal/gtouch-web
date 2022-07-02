
from django.urls import path
 
# importing views from views..py
from .views import home_view,live_view
 
urlpatterns = [
    path('', home_view),
    path('live', live_view),
]