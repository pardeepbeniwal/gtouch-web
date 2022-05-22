from django.db import models
from django.core.validators import FileExtensionValidator
from .utils import get_video_duration, get_thumbnail
from django.db.models import signals
from django.dispatch import receiver

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimestampMixin):
    class DelType(models.IntegerChoices):
        NOT_DELETE = 0, "NOT_DELETE"
        DELETED = 1, "DELETED"
    
    class Status(models.IntegerChoices):
        NOT_ACTIVE = 0, "NOT_ACTIVE"
        ACTIVE = 1, "ACTIVE"

    class Meta:
        verbose_name_plural = "Category"

    name = models.CharField(max_length=255, unique=True)
    is_delete = models.IntegerField(choices=DelType.choices, default=0)
    status = models.IntegerField(choices=Status.choices, default=1)

    def __str__(self):
        return f"{self.name}"

class VideoModel(TimestampMixin):
    video_file_ext = ['WEBM','MPG','MP2','MPEG','MPE','MPV','OGG','MP4','M4P','M4V','AVI','WMV','MOV','QT','FLV','SWF']

    class DelType(models.IntegerChoices):
        NOT_DELETE = 0, "NOT_DELETE"
        DELETED = 1, "DELETED"
    
    class Status(models.IntegerChoices):
        NOT_ACTIVE = 0, "NOT_ACTIVE"
        ACTIVE = 1, "ACTIVE"

    class Meta:
        verbose_name_plural = "Video"
        verbose_name = "Video"

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_constraint=False, related_name='category')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video_file = models.FileField(upload_to='video_files/',blank=True, validators=[FileExtensionValidator(allowed_extensions=video_file_ext)])
    duration = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)
    is_delete = models.IntegerField(choices=DelType.choices, default=0)
    status = models.IntegerField(choices=Status.choices, default=1)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        super(VideoModel, self).save(*args, **kwargs)
    

@receiver(signals.post_save, sender=VideoModel)
def video_modify(sender, instance, created, **kwargs):
    if created:
        instance.duration = get_video_duration(instance.video_file)
        instance.thumbnail = get_thumbnail(instance.video_file)        
        instance.save()