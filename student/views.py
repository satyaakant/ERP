from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, CustomSession
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
import uuid
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Custom login view for students using enrollment number
def login(request):
    if request.method == 'POST':
        enroll_number = request.POST['enroll_number'].strip()  # Get the enrollment number
        password = request.POST['password']

        logger.debug(f"Attempting login for enrollment number: {enroll_number}")

        try:
            student = Student.objects.get(enroll_number=enroll_number)
            
            # Ensure the password is hashed
            if not student.password.startswith('pbkdf2_sha256$'):
                student.password = make_password(student.password)
                student.save()

            if check_password(password, student.password):
                # Create a custom session for the student
                session = CustomSession.objects.create(
                    student=student,
                    usertype='student',
                    userdata={'last_login': str(timezone.now())},
                    jwttoken=uuid.uuid4()
                )

                # Store session data in Django's session framework
                request.session['student_id'] = student.id
                request.session['student_name'] = student.name
                request.session['jwttoken'] = str(session.jwttoken)

                # Redirect to the dashboard
                logger.debug(f"User authenticated: {student.name}")
                return redirect('dashboard')
            else:
                logger.warning(f"Invalid password attempt for enrollment number: {enroll_number}")
                return render(request, 'student/login.html', {'error': "Invalid password."})
        except Student.DoesNotExist:
            logger.warning(f"Login attempt with invalid enrollment number: {enroll_number}")
            return render(request, 'student/login.html', {'error': "Invalid enrollment number."})
    else:
        return render(request, 'student/login.html')

# Dashboard view for students
def dashboard(request):
    student_name = request.session.get('student_name')  # Retrieve student name from the session
    if student_name:
        logger.debug(f"User {student_name} accessed the dashboard")
        return render(request, 'student/dashboard.html', {'student_name': student_name})
    else:
        logger.warning("No student name found in session, redirecting to login")
        return redirect('login')
