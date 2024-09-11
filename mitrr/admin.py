from django.contrib import admin
from .models import User, CustomSession, StudentList, TeacherList, Attendance, Subject, TimeTable, Exam, Result, Notification, Event, AttendanceReport, Batch

# Register your models here.

# User admin
admin.site.register(User)

# Custom session admin
admin.site.register(CustomSession)

# StudentList admin
class StudentListAdmin(admin.ModelAdmin):
    list_display = ('name', 'enroll_number', 'section', 'sem', 'email_id', 'batch')  # Display relevant fields
    list_filter = ( 'section', 'batch')  # Filter by year, section, and batch
    search_fields = ('name', 'enroll_number', 'email_id')  # Allow searching by name, enrollment number, and email

admin.site.register(StudentList, StudentListAdmin)

# TeacherList admin
class TeacherListAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_id', 'email_id')  # Display teacher details
    search_fields = ('name', 'teacher_id', 'email_id')  # Allow searching by name, teacher ID, and email

admin.site.register(TeacherList, TeacherListAdmin)

# Batch admin
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_name', 'description', 'semester')  # Display batch details
    search_fields = ('batch_name', 'description')  # Allow searching by batch name and description

admin.site.register(Batch, BatchAdmin)

# Subject admin
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'semester')  # Display subject details
    search_fields = ('name', 'code')  # Allow searching by subject name and code

admin.site.register(Subject, SubjectAdmin)

# Attendance admin
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'batch', 'section', 'semester')  # Display attendance details
    list_filter = ('batch', 'section', 'status', 'subject', 'semester')  # Filter by batch, section, and other fields
    search_fields = ('student__name', 'student__enroll_number')  # Allow searching by student name and enrollment number

admin.site.register(Attendance, AttendanceAdmin)

# TimeTable admin
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'day_of_week', 'semester', 'batch', 'start_time', 'end_time')  # Display timetable details

admin.site.register(TimeTable, TimeTableAdmin)

# Exam admin
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'subject', 'date', 'start_time', 'end_time', 'semester', 'batch', 'total_marks', 'academic_year')  # Display exam details
    search_fields = ('exam_name', 'subject__name', 'batch')  # Allow searching by exam name, subject, and batch

admin.site.register(Exam, ExamAdmin)

# Result admin
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject', 'marks_obtained', 'grade', 'remarks')  # Display result details
    search_fields = ('student__name', 'exam__exam_name', 'subject__name')  # Allow searching by student name, exam name, and subject name

admin.site.register(Result, ResultAdmin)

# Notification admin
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'receiver', 'created_at', 'is_read')  # Display notification details
    search_fields = ('title', 'receiver__username')  # Allow searching by title and receiver username

admin.site.register(Notification, NotificationAdmin)

# Event admin
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'description', 'date', 'start_time', 'end_time', 'location')  # Display event details
    search_fields = ('event_name', 'description', 'location')  # Allow searching by event name, description, and location

admin.site.register(Event, EventAdmin)

# Attendance Report admin
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'total_days', 'days_present', 'percentage', 'semester')  # Display attendance report details
    search_fields = ('student__name', 'student__enroll_number')  # Allow searching by student name and enrollment number

admin.site.register(AttendanceReport, AttendanceReportAdmin)
