# Generated by Django 4.0.4 on 2022-05-21 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_file', models.FileField(blank=True, upload_to='')),
                ('video_time', models.CharField(blank=True, max_length=255, null=True)),
                ('is_delete', models.IntegerField(choices=[(0, 'NOT_DELETE'), (1, 'DELETED')], default=0)),
                ('status', models.IntegerField(choices=[(0, 'NOT_ACTIVE'), (1, 'ACTIVE')], default=1)),
                ('category', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='video.category')),
            ],
            options={
                'verbose_name_plural': 'Category',
            },
        ),
    ]
