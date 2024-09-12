from django.urls import path
from . import views

urlpatterns = [
    # Student-related endpoints
    path('mitrr/students/', views.getStudentList_Mitrr, name='get-student-list-mitrr'),  
    path('mitrr/students/add/', views.addStudentList_Mitrr, name='add-student-list-mitrr'), 
    path('mitrr/students/delete/<str:enroll_number>/', views.deleteStudent_Mitrr, name='delete-student-mitrr'),

    # Teacher-related endpoints
    path('mitrr/teachers/', views.getTeacherList_Mitrr, name='get-teacher-list-mitrr'),  
    path('mitrr/teachers/add/', views.addTeacherList_Mitrr, name='add-teacher-list-mitrr'),  
    path('mitrr/teachers/delete/<str:teacher_id>/', views.deleteTeacher_Mitrr, name='delete-teacher-mitrr'),

    # Attendance-related endpoints
    path('getAttendance/', views.getAttendanceList_Mitrr, name='get-attendance-list-mitrr'),
    path('attendance/add/', views.addAttendance, name='add-attendance'),
    
    # Timetable-related endpoints
    path('timetable/', views.getTimetable, name='get-timetable'),
    path('timetable/add/', views.addTimetable, name='add-timetable'),

    # Exam-related endpoints
    path('exams/', views.getExamList, name='get-exam-list'),
    path('exams/add/', views.addExam, name='add-exam'),
    path('exams/delete/<int:pk>/', views.deleteExam, name='delete-exam'),

    # Result-related endpoints
    path('results/', views.getResultList, name='get-result-list'),
    path('results/add/', views.addResult, name='add-result'),
    path('results/delete/<int:pk>/', views.deleteResult, name='delete-result'),

    # Notification-related endpoints
    path('notifications/', views.getNotificationList, name='get-notification-list'),
    path('notifications/add/', views.addNotification, name='add-notification'),
    path('notifications/delete/<int:pk>/', views.deleteNotification, name='delete-notification'),

    # Event-related endpoints
    path('events/', views.getEventList, name='get-event-list'),
    path('events/add/', views.addEvent, name='add-event'),
    path('events/delete/<int:pk>/', views.deleteEvent, name='delete-event'),

    # Attendance Report-related endpoints
    path('attendance-reports/', views.getAttendanceReportList, name='get-attendance-report-list'),
    path('attendance-reports/add/', views.addAttendanceReport, name='add-attendance-report'),
    path('attendance-reports/delete/<int:pk>/', views.deleteAttendanceReport, name='delete-attendance-report'),

    # Batch-related endpoints
    path('batches/', views.getBatchList, name='get-batch-list'),
    path('batches/add/', views.addBatch, name='add-batch'),
    path('batches/delete/<int:pk>/', views.deleteBatch, name='delete-batch'),


        path('mitrr/subjects/', views.getSubjectsBySemester, name='get-subjects-by-semester'),

]
