# Generated by Django 3.2.5 on 2022-09-16 15:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20220916_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='create_date',
        ),
        migrations.AddField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 53, 14, 250150, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 53, 14, 252145, tzinfo=utc)),
        ),
    ]
