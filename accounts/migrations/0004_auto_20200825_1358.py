# Generated by Django 3.1 on 2020-08-25 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200822_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='comments',
            field=models.TextField(default='comments_default_pyshell'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(unique=True, upload_to=''),
        ),
    ]
