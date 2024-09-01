from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("teacher/", views.teacher, name="teacher"),
    path("student/", views.student, name="student"),
    
    # rest
    path("rest/add-teacher/", views.add_teacher, name="add-teacher"),
    path("rest/add-student/", views.add_student, name="add-student"),

]