# Generated by Django 4.0.4 on 2022-06-16 14:07

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0022_alter_category_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 14, 7, 21, 884744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='favoritvideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 14, 7, 21, 884744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='live',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 14, 7, 21, 884744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 14, 7, 21, 884744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sections',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 14, 7, 21, 884744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 14, 7, 21, 884744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 16, 14, 7, 21, 884744, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(upload_to='static/video_thumbnail/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['.bmp', '.jpe', '.jpg', '.jpeg', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm'])]),
        ),
    ]