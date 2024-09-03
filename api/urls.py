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
    path('attendance/<int:year>/', views.getAttendanceList_Mitrr, name='get-attendance-list-mitrr'),  # Year is now an integer like 1, 2, 3, 4
    path('attendance/add/', views.addAttendance, name='add-attendance'),
    path('attendance/filter/', views.getFilteredAttendanceList, name='get-filtered-attendance'),
]
