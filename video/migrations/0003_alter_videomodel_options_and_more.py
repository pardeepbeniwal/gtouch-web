# Generated by Django 4.0.4 on 2022-05-21 11:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_videomodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videomodel',
            options={'verbose_name_plural': 'Video'},
        ),
        migrations.RenameField(
            model_name='videomodel',
            old_name='video_time',
            new_name='duration',
        ),
        migrations.AddField(
            model_name='videomodel',
            name='thumbnail',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='videomodel',
            name='video_file',
            field=models.FileField(blank=True, upload_to='video_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['WEBM', 'MPG', 'MP2', 'MPEG', 'MPE', 'MPV', 'OGG', 'MP4', 'M4P', 'M4V', 'AVI', 'WMV', 'MOV', 'QT', 'FLV', 'SWF'])]),
        ),
    ]
