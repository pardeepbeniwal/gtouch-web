# Generated by Django 4.0.4 on 2022-05-31 12:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_remove_video_show_on_home_alter_category_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 12, 21, 23, 671446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='favoritvideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 12, 21, 23, 671446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='live',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 12, 21, 23, 671446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 12, 21, 23, 671446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sections',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 12, 21, 23, 671446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 12, 21, 23, 671446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 31, 12, 21, 23, 671446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_type',
            field=models.IntegerField(choices=[(1, 'NORMAL'), (2, 'SERIES')], default=1),
        ),
    ]
