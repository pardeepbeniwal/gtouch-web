# Generated by Django 4.0.4 on 2022-06-17 08:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_usersession_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 17, 8, 44, 45, 877466, tzinfo=utc)),
        ),
    ]