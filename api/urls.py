from django.urls import path
from . import views

urlpatterns = [
    # mitrr pov
    path('mitrr/students/', views.getStudentList_Mitrr, name='get-student-list-mitrr'),  
    path('mitrr/students/add/', views.addStudentList_Mitrr, name='add-student-list-mitrr'), 
    path('mitrr/teachers/', views.getTeacherList_Mitrr, name='get-teacher-list-mitrr'),  
    path('mitrr/teachers/add/', views.addTeacherList_Mitrr, name='add-teacher-list-mitrr'),  
 # Delete endpoints
    path('mitrr/students/delete/<str:enroll_number>/', views.deleteStudent_Mitrr, name='delete-student-mitrr'),
    path('mitrr/teachers/delete/<str:teacher_id>/', views.deleteTeacher_Mitrr, name='delete-teacher-mitrr'),
    #attendance
        path('attendance/', views.getAttendanceList_Mitrr,name='get-attendance-list-mitrr'),

]