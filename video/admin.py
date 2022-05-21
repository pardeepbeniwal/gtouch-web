from django.contrib import admin
from video.models import Category, VideoModel

admin.site.site_header = "Gtouch Admin"
admin.site.site_title = "Gtouch Admin Portal"
admin.site.index_title = "Welcome to Gtouch Admin Portal"



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_delete')

class VideoAdmin(admin.ModelAdmin):
    exclude = ('duration', 'thumbnail')
    list_display = ('title', 'category', 'description', 'status', 'is_delete')

admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoModel, VideoAdmin)