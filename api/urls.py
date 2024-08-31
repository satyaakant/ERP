from django.urls import path
from . import views

urlpatterns = [
    path('admin/students/', views.getStudentList, name='get-student-list-admin'),  
    path('admin/students/add/', views.addStudentList, name='add-student-list-admin'), 
    path('admin/teachers/', views.getTeacherList, name='get-teacher-list-admin'),  
    path('admin/teachers/add/', views.addTeacherList, name='add-teacher-list-admin'),  
]