from django.contrib import admin
from video.models import ( 
            Category, Video, Sections, HomePage, 
            Live, News
)
from django.utils.html import mark_safe

admin.site.site_header = "Gtouch Admin"
admin.site.site_title = "Gtouch Admin Portal"
admin.site.index_title = "Welcome to Gtouch Admin Portal"


class SectionsAdmin(admin.ModelAdmin):
    list_display = ('name','status',)
    exclude = ('slug', 'is_delete','created_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status',)
    exclude = ('slug', 'is_delete','created_at')


class HomePageAdmin(admin.ModelAdmin):
    exclude = ('duration', 'is_delete','created_at')
    list_display = ('title', 'category', 'description','img_thumbnail', 'duration','sections', 'status',)
    #form = HomePageForm

    def img_thumbnail(self, obj):
        if obj.v_thumbnail:
            return mark_safe(
                    '<img src="https://gtouch.s3.amazonaws.com/%s" style="max-width:250px;max-height:250px"/>'
                    % (obj.v_thumbnail)
            )
    img_thumbnail.allow_tags = True
    img_thumbnail.short_description = "Image"


class NewsAdmin(admin.ModelAdmin):
    exclude = ('created_at',)
    list_display = ('title','url','description','status')


class LiveAdmin(admin.ModelAdmin):
    exclude = ('created_at',)
    list_display = ('title','url','img_thumbnail','status')


    def img_thumbnail(self, obj):
        if obj.thumbnail:
            return mark_safe(
                    '<img src="https://gtouch.s3.amazonaws.com/%s" style="max-width:250px;max-height:250px"/>'
                    % (obj.thumbnail)
            )
    img_thumbnail.allow_tags = True
    img_thumbnail.short_description = "Image"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Sections, SectionsAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Live, LiveAdmin)
