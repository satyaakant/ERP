from django.urls import path
from . import views

urlpatterns = [
    path('admin/students/', views.getStudentListAdmin, name='get-student-list-admin'),  
    path('admin/students/add/', views.addStudentListAdmin, name='add-student-list-admin'), 
    path('admin/teachers/', views.getTeacherListAdmin, name='get-teacher-list-admin'),  
    path('admin/teachers/add/', views.addTeacherListAdmin, name='add-teacher-list-admin'),  
]