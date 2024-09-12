from django.urls import path
from . import views

urlpatterns = [
    path('take-attendance/', views.take_attendance, name='take_attendance'),
    ]