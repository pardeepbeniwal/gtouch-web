# Generated by Django 4.0.4 on 2022-05-28 08:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0007_sections_alter_category_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Live',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 23, 42, 283846, tzinfo=utc))),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('status', models.IntegerField(choices=[(0, 'NOT_ACTIVE'), (1, 'ACTIVE')], default=1)),
                ('thumbnail', models.ImageField(upload_to='live_thumbnail/')),
            ],
            options={
                'verbose_name_plural': 'news',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 23, 42, 283846, tzinfo=utc))),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('status', models.IntegerField(choices=[(0, 'NOT_ACTIVE'), (1, 'ACTIVE')], default=1)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'news',
            },
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('video.video',),
        ),
        migrations.RemoveField(
            model_name='video',
            name='url',
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 23, 42, 283846, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='favoritvideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 23, 42, 283846, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sections',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 23, 42, 283846, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 23, 42, 283846, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 8, 23, 42, 283846, tzinfo=utc)),
        ),
    ]
