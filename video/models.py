from django.utils import timezone
from django.db import models
from django.core.validators import FileExtensionValidator

from account.models import User
from .utils import get_video_duration, get_thumbnail
from django.db.models import signals
from django.dispatch import receiver

class Status(models.IntegerChoices):
    NOT_ACTIVE = 0, "NOT_ACTIVE"
    ACTIVE = 1, "ACTIVE"
    
class DelType(models.IntegerChoices):
    NOT_DELETE = 0, "NOT_DELETE"
    DELETED = 1, "DELETED"

class VideoTypes(models.IntegerChoices):
    NORMAL = 1, "NORAMAL"
    SERIES = 2, "SERIES"

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimestampMixin):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True, null=True)
    #parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=Status.choices, default=1)
    is_delete = models.IntegerField(choices=DelType.choices, default=0)

    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return f"{self.name}"

class Sections(TimestampMixin):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=1)
    is_delete = models.IntegerField(choices=DelType.choices, default=0)

    class Meta:
        verbose_name_plural = "sections"
    
    def __str__(self):
        return f"{self.name}"


class CommonInfo(TimestampMixin):
    title = models.CharField(max_length=255,blank=False)
    url = models.URLField(blank=False)
    status = models.IntegerField(choices=Status.choices, default=1)

    class Meta:
        abstract = True


class News(CommonInfo):
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "news"


class Live(CommonInfo):
    thumbnail = models.ImageField(upload_to='live_thumbnail/')

    class Meta:
        verbose_name_plural = "live"


class Video(TimestampMixin):
    video_file_ext = ['WEBM','MPG','MP2','MPEG','MPE','MPV','OGG','MP4','M4P','M4V','AVI','WMV','MOV','QT','FLV','SWF']

    class Meta:
        verbose_name_plural = "Video"
        verbose_name = "Video"

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_constraint=False, related_name='category')
    section = models.ManyToManyField(Sections,related_name='sections', blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video_file = models.FileField(upload_to='video_files/',blank=False, validators=[FileExtensionValidator(allowed_extensions=video_file_ext)])
    duration = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)
    is_delete = models.IntegerField(choices=DelType.choices, default=0)
    status = models.IntegerField(choices=Status.choices, default=1)
    cast_details = models.TextField(null=True,blank=True)
    video_type = models.IntegerField(choices=VideoTypes.choices,default=1)
    

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def sections(self):
        return "\n".join([p.name for p in self.section.all()])

class HomePage(Video):
    class Meta:
        proxy = True

class FavoritVideo(TimestampMixin):
    class Meta:
        verbose_name_plural = "Favorit Video"

    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING, db_constraint=False, related_name='fav_video')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name='fav_user')

    def __str__(self):
        return f"{self.id}"

class UserHistory(TimestampMixin):

    class Meta:
        verbose_name_plural = "User History"

    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING, db_constraint=False, related_name='user_history_video')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name='history_user')
    watch_duration_time = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.video}"


@receiver(signals.post_save, sender=HomePage)
def video_modify(sender, instance, created, **kwargs):
    if created:
        instance.duration = get_video_duration(instance.video_file)
        instance.thumbnail = get_thumbnail(instance.video_file)
        instance.save()