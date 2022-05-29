# Generated by Django 4.0.4 on 2022-05-28 08:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0012_alter_category_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='show_on_home',
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 55, 7, 304504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='favoritvideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 55, 7, 304504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='live',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 55, 7, 304504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 55, 7, 304504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sections',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 55, 7, 304504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 55, 7, 304504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 55, 7, 304504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='section',
            field=models.ManyToManyField(blank=True, related_name='sections', to='video.sections'),
        ),
    ]