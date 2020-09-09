"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import  *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', Home, name='home'),
    path('register/teacher', TeacherSignUpView.as_view(), name='teacher_signup'),
    path('register/student', StudentSignUpView.as_view(), name='student_signup'),

    path('register/classroom', ClassroomCreateView.as_view(), name='classroom_create'),
    path('join/classroom', ClassroomJoinView.as_view(), name='classroom_join'),

    path('', ClassroomListView.as_view(), name='list_classrooms'),
    path('detailclassroom/<int:pk>', ClassroomDetailView.as_view(), name='classroom_detail'),

    path('register/video', VideoCreateView.as_view(), name='video_create'),
    path('register/video<int:classroom_pk>', VideoCreateView.as_view(), name='video_create'),
    path('v/<int:pk>', VideoDetailView.as_view(), name='video_detail'),

    path('logoutsuccess/', LogoutSuccessView, name='logout_success'),
    path('s3direct/', include('s3direct.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
