# Generated by Django 3.1 on 2020-08-25 08:56

from django.db import migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200825_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=s3direct.fields.S3DirectField(unique=True),
        ),
    ]
