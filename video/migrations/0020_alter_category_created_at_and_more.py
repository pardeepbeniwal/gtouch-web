# Generated by Django 4.0.4 on 2022-06-04 06:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0019_alter_category_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 26, 9, 630617, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='favoritvideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 26, 9, 630617, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='live',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 26, 9, 630617, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 26, 9, 630617, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sections',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 26, 9, 630617, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 26, 9, 630617, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 4, 6, 26, 9, 630617, tzinfo=utc)),
        ),
    ]
