import imp
from django.shortcuts import render

from video.api.serializers import LiveSerializer
from video.models import Live,Video
from django.conf import settings
cloud_front_url = settings.CLOUD_FRONT_URL

def convert_sec_to_hr(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%dh% 02dm" % (hour, min)

def get_carousel_data():
    data = []
    records = Video.objects.filter(section__name='Carousel').order_by("-id")[:5]
    for rec in records:
        inner = {}
        inner['entryid'] = str(rec.id)
        inner['imgurl'] = cloud_front_url+str(rec.v_thumbnail.name)
        inner['priority'] = 1
        inner['description'] = rec.description
        inner['duration'] = convert_sec_to_hr(int(rec.duration))
        data.append(inner)
    return data

def home_view(request):
    queryset = Live.objects.all().order_by('-id')[:30]
    live_data = LiveSerializer(queryset, many=True).data
    context ={
        "live_data": live_data,
        "carousal_data": get_carousel_data()
    }
    # return response with template and context
    return render(request, "home.html", context)

def live_view(request):
    queryset = Live.objects.all().order_by('-id')[:30]
    live_data = LiveSerializer(queryset, many=True).data
    context ={
        "live_data": live_data
    }
    # return response with template and context
    return render(request, "live.html", context)

def live_series(request):
    queryset = Live.objects.all().order_by('-id')[:30]
    live_data = LiveSerializer(queryset, many=True).data
    context ={
        "live_data": live_data
    }
    # return response with template and context
    return render(request, "live.html", context)