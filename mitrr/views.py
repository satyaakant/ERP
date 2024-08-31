import requests
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(requests):
    return render(requests, 'mitrr/login.html')

def dashboard(requests):
    return render(requests, 'mitrr/dashboard.html')

def teacher(requests):
    return render(requests, 'mitrr/teacher.html')

def student(requests):
    return render(requests, 'mitrr/student.html')
