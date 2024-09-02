from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, CustomSession
from django.utils import timezone
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Custom login view for students using enrollment number
def login(request):
    if request.method == 'POST':
        enroll_number = request.POST['enroll_number'] 
        password = request.POST['password']
        print(enroll_number)
        student = Student.objects.filter(enroll_number=enroll_number)
        stored_password = student.password 
        print(stored_password)
        
    return render(request, 'student/login.html')

# Dashboard view for students
def dashboard(request):
    return render(request, 'student/dashboard.html')
    # student_name = request.session.get('student_name')  # Retrieve student name from the session
    # if student_name:
    #     logger.debug(f"User {student_name} accessed the dashboard")
    #     return render(request, 'student/dashboard.html', {'student_name': student_name})
    # else:
    #     logger.warning("No student name found in session, redirecting to login")
    #     return redirect('login')
