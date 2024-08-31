from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request, 'mitrr/login.html')

def dashboard(request):
    return render(request, 'mitrr/dashboard.html')

def teacher(request):
    return render(request, 'mitrr/teacher.html')

def student(request):
    return render(request, 'mitrr/student.html')
