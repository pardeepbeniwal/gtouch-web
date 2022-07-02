# Generated by Django 4.0.4 on 2022-06-02 16:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0015_alter_category_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 16, 9, 52, 33423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='favoritvideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 16, 9, 52, 33423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='live',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 16, 9, 52, 33423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 16, 9, 52, 33423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sections',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 16, 9, 52, 33423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 16, 9, 52, 33423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 16, 9, 52, 33423, tzinfo=utc)),
        ),
    ]
