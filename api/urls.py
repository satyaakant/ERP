from django.urls import path
from . import views

urlpatterns = [
    path('admin/students/', views.getStudentListAdmin, name='get-student-list-admin'),    
]