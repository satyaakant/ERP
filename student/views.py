import requests
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        enroll_number = request.POST.get('enroll_number')
        password = request.POST.get('password')

        # Construct the URL to make the API call
        url = "http://127.0.0.1:8000/api/mitrr/students/"
        
        # Make an API call to get the student list
        response = requests.get(url)
        
        if response.status_code == 200:
            students = response.json()

            # Specific student lookup
            student = next((s for s in students if s['enroll_number'] == enroll_number and s['password'] == password), None)
            
            if student:
                # Store necessary information in the session
                request.session['student_id'] = student['id']
                request.session['student_name'] = student['name']

                # Redirect to the dashboard
                return redirect('/dashboard/')
            else:
                messages.error(request, "Invalid enrollment number or password.")
                return render(request, 'student/login.html')
        else:
            messages.error(request, "Failed to fetch students from API.")
            return render(request, 'student/login.html')

    return render(request, 'student/login.html')

def dashboard(request):
    student_name = request.session.get('student_name', 'Guest')
    return render(request, 'student/dashboard.html', {'student_name': student_name})
