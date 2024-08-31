from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("teacher/", views.teacher, name="teacher"),
    path("student/", views.student, name="student"),
]