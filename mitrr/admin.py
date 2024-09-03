from django.contrib import admin
from .models import User, CustomSession, StudentList, TeacherList, Attendance, Subject

# Register your models here.

admin.site.register(User)
admin.site.register(CustomSession)
class StudentListAdmin(admin.ModelAdmin):
    list_display = ('name', 'enroll_number', 'year', 'section', 'sem', 'email_id')
    list_filter = ('year', 'section')  # Filter by year and section
    search_fields = ('name', 'enroll_number', 'email_id')

admin.site.register(StudentList, StudentListAdmin)

class TeacherListAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_id', 'email_id')
    search_fields = ('name', 'teacher_id', 'email_id')

admin.site.register(TeacherList, TeacherListAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'semester', 'year')
    search_fields = ('name', 'code')

admin.site.register(Subject, SubjectAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'year', 'section')
    list_filter = ('year', 'section', 'status', 'subject')  # Filter by year, section, status, and subject
    search_fields = ('student__name', 'student__enroll_number')

admin.site.register(Attendance, AttendanceAdmin)
