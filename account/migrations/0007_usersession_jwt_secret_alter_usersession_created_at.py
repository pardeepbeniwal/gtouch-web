# Generated by Django 4.0.4 on 2022-06-02 17:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_usersession_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 17, 7, 51, 322178, tzinfo=utc)),
        ),
    ]
