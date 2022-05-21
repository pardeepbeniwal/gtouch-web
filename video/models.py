from django.db import models
from django.core.validators import FileExtensionValidator


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

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_constraint=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video_file = models.FileField(upload_to='video_files/',blank=True, validators=[FileExtensionValidator(allowed_extensions=video_file_ext)])
    duration = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)
    is_delete = models.IntegerField(choices=DelType.choices, default=0)
    status = models.IntegerField(choices=Status.choices, default=1)

    def __str__(self):
        return f"{self.title}"