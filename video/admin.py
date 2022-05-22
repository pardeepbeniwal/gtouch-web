from django.contrib import admin
from video.models import Category, VideoModel

admin.site.site_header = "Gtouch Admin"
admin.site.site_title = "Gtouch Admin Portal"
admin.site.index_title = "Welcome to Gtouch Admin Portal"


from django.utils.html import mark_safe
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_delete')

class VideoAdmin(admin.ModelAdmin):
    exclude = ('duration', 'thumbnail')
    list_display = ('title', 'category', 'description','img_thumbnail', 'duration', 'status', 'is_delete')
    
    def img_thumbnail(self, obj):        
        if obj.thumbnail:
            return mark_safe(
                    '<img src="https://gtouch-static.s3.amazonaws.com/%s" style="max-width:250px;max-height:250px"/>'
                    % (obj.thumbnail)
            )
    img_thumbnail.allow_tags = True
    img_thumbnail.short_description = "Find Image"

admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoModel, VideoAdmin)