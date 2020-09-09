from django.db import models
import os

from django.contrib.auth.models import AbstractUser

from s3direct.fields import S3DirectField
from django.conf import settings

from shortuuidfield import ShortUUIDField

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100,blank=False, null=False)
    roll_no = models.IntegerField(unique=True)
    join_year = models.IntegerField()
    email = models.EmailField(unique=True)

    student_created_time = models.DateField(auto_now=False, auto_now_add=True)
    student_updated_time = models.DateField(auto_now=True, auto_now_add=False)

    BCS = 'BCS'
    IPG = 'IPG'
    IMG = 'IMG'
    COURSE_CHOICES = [
        (BCS, 'BCS'),
        (IPG, 'IPG'),
        (IMG, 'IMG'),
    ]
    course = models.CharField(
        max_length=3,
        choices=COURSE_CHOICES,
        blank=False, null=True
    )


    def __str__(self):
        return self.full_name

class Teacher(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    teacher_created_time = models.DateField(auto_now=False, auto_now_add=True)
    teacher_updated_time = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.full_name

class Classroom(models.Model):
    small_uuid = ShortUUIDField()
    classroom_name = models.CharField(max_length=50, unique=True)
    classroom_teacher = models.ForeignKey('User',on_delete=models.CASCADE, related_name='classroom_teachers')
    classroom_student = models.ManyToManyField('User', related_name='classroom_students', blank=True)

    classroom_created_time = models.DateField(auto_now=False, auto_now_add=True)
    classroom_updated_time = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.classroom_name

class Video(models.Model):
    video_title = models.CharField(max_length=40)
    video_file = S3DirectField(unique=True,dest='primary_destination')
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, related_name='videos')
    comments = models.TextField(blank=True,default='')
    video_created_time = models.DateField(auto_now=False, auto_now_add=True)
    video_updated_time = models.DateField(auto_now=True, auto_now_add=False)

    @property
    def filename(self):
        # if self.video_file.startswith('http'):
        #     cut = len(settings.AWS_S3_ENDPOINT_URL)+len('/') + len(settings.AWS_STORAGE_BUCKET_NAME)+len('/')
        #     cut += len('input/')  # obtained from primary destination
        #     return self.video_file[cut:]
        # else:
        #     return self.video_file
        return self.video_file
    
    @property
    def filename_without_extension(self):

        filename_with_extension = self.filename
        # cut_file_extension_index = 0
        # for c in reversed(filename_with_extension):
        #     cut_file_extension_index+=1
        #     if c=='.':
        #         break
        # if cut_file_extension_index<6:
        #     return filename_with_extension[:cut_file_extension_index]
        # else:
        #     return filename_with_extension
        return filename_with_extension

    def __str__(self):
        return self.filename_without_extension

