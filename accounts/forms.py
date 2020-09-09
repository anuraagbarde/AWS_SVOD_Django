from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from django import forms
from s3direct.widgets import S3DirectWidget
from django.conf import settings

import re

from .models import *

class TeacherSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=Subject.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True, max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()

        
        email_form = self.cleaned_data['email'], #this is returning ('t17@gmail.com',) instead of t17@gmail.com #solution= cleaned_data['email'] returns a tuple
        full_name_form = self.cleaned_data['full_name']
        teacher = Teacher.objects.create(user=user, email=email_form[0], full_name=full_name_form )
        # student.interests.add(*self.cleaned_data.get('interests'))
        return user
    
class StudentSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=Subject.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )
    
    BCS = 'BCS'
    IPG = 'IPG'
    IMG = 'IMG'
    COURSE_CHOICES = [
        (BCS, 'BCS'),
        (IPG, 'IPG'),
        (IMG, 'IMG'),
    ]

    full_name           = forms.CharField(required=True, max_length=100)
    roll_no             = forms.IntegerField(required=True)
    join_year           = forms.IntegerField(required=True)
    email               = forms.EmailField(required=True)
    course              = forms.ChoiceField(choices=COURSE_CHOICES,required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()

        full_name_form = self.cleaned_data['full_name']
        roll_no_form = self.cleaned_data['roll_no']
        join_year_form = self.cleaned_data['join_year']
        email_form = self.cleaned_data['email'], #this is returning ('t17@gmail.com',) instead of t17@gmail.com #solution= cleaned_data['email'] returns a tuple
        course_form = self.cleaned_data['course']

        student = Student.objects.create(
                                        user=user,
                                        full_name=full_name_form,
                                        roll_no=roll_no_form, 
                                        join_year=join_year_form, 
                                        email=email_form[0], 
                                        course=course_form
                                        )

        # student.interests.add(*self.cleaned_data.get('interests'))
        return user


class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ('classroom_name',)

class ClassroomJoinForm(forms.Form):
    unverified_classcode = forms.CharField(min_length=22,max_length=22, label="Classroom Code")

    def clean_unverified_classcode(self):
        data = self.cleaned_data['unverified_classcode']
        if not Classroom.objects.filter(small_uuid = data).exists():
            raise forms.ValidationError("The classroom with the given code does not exist!")
        
        return data
    
class VideoCreateForm(forms.ModelForm):
    video_file = forms.URLField(widget=S3DirectWidget(dest='primary_destination'))
    
    def form_filename(self):
        cut = len(settings.AWS_S3_ENDPOINT_URL)+len('/') + len(settings.AWS_STORAGE_BUCKET_NAME)+len('/')
        cut += len('input/')  # obtained from primary destination

        file_url = self.cleaned_data['video_file']
        cut_file_extension = 0
        for c in reversed(file_url):
            cut_file_extension+=1
            if c=='.':
                break
        cut_file_extension = len(file_url) - cut_file_extension

        fileurl_without_extension = file_url[:cut_file_extension]
        
        return fileurl_without_extension[cut:]
 
    def clean_video_file(self):
        data = self.form_filename()
        print('data = ' + data)
        # if not data.isalnum():
        if not re.match(r'^\w+$', data):
            raise forms.ValidationError("The file name should only contain letters and numbers, NO SPACES or SPECIAL CHARACTERS!")
        return data
    
    class Meta:
        model = Video
        fields = ('video_title','video_file','comments')
