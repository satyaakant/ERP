from django.contrib import admin
from .models import User, CustomSession, StudentList, TeacherList, Attendance, Subject, TimeTable, Exam, Result, Notification,  Event, AttendanceReport, Batch

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
    list_display = ('student', 'subject', 'date', 'status', 'year', 'section', 'semester')
    list_filter = ('year', 'section', 'status', 'subject', 'semester') 
    search_fields = ('student__name', 'student__enroll_number')

admin.site.register(Attendance, AttendanceAdmin)

class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'day_of_week', 'semester', 'batch', 'start_time', 'end_time')

admin.site.register(TimeTable, TimeTableAdmin)

class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'subject', 'date', 'start_time', 'end_time', 'semester', 'batch', 'total_marks', 'academic_year')
    search_fields = ('exam_name', 'subject__name', 'batch')

admin.site.register(Exam, ExamAdmin)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject', 'marks_obtained', 'grade', 'remarks')
    search_fields = ('student__name', 'exam__exam_name', 'subject__name')

admin.site.register(Result, ResultAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'receiver', 'created_at', 'is_read')
    search_fields = ('title', 'receiver__username')

admin.site.register(Notification, NotificationAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'description', 'date', 'start_time', 'end_time', 'location')
    search_fields = ('event_name', 'description', 'location')

admin.site.register(Event, EventAdmin)


class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'total_days', 'days_present', 'percentage', 'semester')
    search_fields = ('student__name', 'student__enroll_number')

admin.site.register(AttendanceReport, AttendanceReportAdmin)

class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_name', 'year', 'description', 'semester')
    search_fields = ('batch_name', 'description')

admin.site.register(Batch, BatchAdmin)
