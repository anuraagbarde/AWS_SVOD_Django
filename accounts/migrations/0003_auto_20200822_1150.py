# Generated by Django 3.1 on 2020-08-22 06:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_classroom_classroom_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='classroom_updated_time',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='student',
            name='student_created_time',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='student_updated_time',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacher_created_time',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacher_updated_time',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_created_time',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='video_updated_time',
            field=models.DateField(auto_now=True),
        ),
    ]
