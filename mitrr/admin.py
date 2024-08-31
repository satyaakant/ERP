from django.contrib import admin
from .models import User, StudentList, TeacherList

# Register your models here.
admin.site.register(User)
admin.site.register(StudentList)
admin.site.register(TeacherList)