from django.contrib import admin
from .models import *

admin.site.register([User,Student,Teacher,Classroom,Video])