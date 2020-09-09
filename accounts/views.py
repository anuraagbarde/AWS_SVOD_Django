from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import teacher_required, student_required


from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView, FormView

from .models import *
from .forms import *


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list_classrooms')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list_classrooms')

@method_decorator([login_required, teacher_required], name='dispatch')
class ClassroomCreateView(CreateView):
    model = Classroom
    form_class = ClassroomCreateForm
    template_name = 'accounts/classroom_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_full_name'] = self.request.user.teacher.full_name
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        classroom_form = form.save(commit=False)
        classroom_form.classroom_teacher = self.request.user
        classroom_form.save()
        return redirect('list_classrooms')


@method_decorator([login_required], name='dispatch')
class ClassroomListView(ListView):
    model = Classroom
    # ordering = ('classroom_name',)
    context_object_name = 'classrooms'
    template_name = 'accounts/classroom_list.html'

    def get_queryset(self):
        if self.request.user.is_teacher:
            return self.request.user.classroom_teachers.all()
        elif self.request.user.is_student:
            return self.request.user.classroom_students.all()

@method_decorator([login_required], name='dispatch')
class ClassroomDetailView(DetailView):
    model = Classroom
    template_name='accounts/classroom_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # if qs.exists():
        if self.request.user.is_teacher:
            return qs.filter(classroom_teacher=self.request.user)
        elif self.request.user.is_student:
            return qs.filter(classroom_student=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = context['object'].videos.all()
        return context

@method_decorator([login_required,student_required], name='dispatch')
class ClassroomJoinView(FormView):
    template_name = 'accounts/classroom_join.html'
    form_class = ClassroomJoinForm

    def form_valid(self, form):
        unverified_code = form.cleaned_data['unverified_classcode']
        qs = Classroom.objects.get(small_uuid = unverified_code)
        qs.classroom_student.add(self.request.user)
        return redirect('list_classrooms')
    
@method_decorator([login_required,teacher_required], name='dispatch')
class VideoCreateView(CreateView):
    model = Video
    form_class = VideoCreateForm
    template_name = 'accounts/video_form.html'

    
    def form_valid(self, form):
        video_form = form.save(commit=False)
        teachers_classrooms = Classroom.objects.filter(classroom_teacher=self.request.user)
        classroom_pk = self.kwargs['classroom_pk']
        video_form.classroom = get_object_or_404(teachers_classrooms, pk = classroom_pk )
        video_form.save()
        return redirect('list_classrooms')

@method_decorator([login_required], name='dispatch')
class VideoDetailView(DetailView):
    model = Video
    template_name = 'accounts/video_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # if qs.exists():
        if self.request.user.is_teacher:
            return qs.filter(classroom__classroom_teacher = self.request.user)
        elif self.request.user.is_student:
            return qs.filter(classroom__classroom_student = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid_url = 'https://d35xdpmdsjhy8w.cloudfront.net/output/dash/' + context['object'].filename_without_extension + '.mpd'
        context['video_url'] = vid_url
        return context
    


def Home(request):
    return HttpResponse('<html><p>this is home</p> </html>')

def LogoutSuccessView(request):
    return render(request,'registration/logout_successful.html' ,{})