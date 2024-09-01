import requests , json , random
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, CustomSession
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)

            # Delete any existing session for the user
            CustomSession.objects.filter(user=user).delete()

            # Create a new session
            customsession = CustomSession.objects.create(
                user=user,
                usertype='mitrr',
                userdata={
                    'name': user.name,
                    'username': user.username,
                    'usertype': 'mitrr',
                    'data':[]
                },
                created_at=timezone.now()
            )
            # store data in session
            request.session['jwttoken'] = str(customsession.jwttoken)
            request.session['userdata'] = str(customsession.userdata)

            return redirect('dashboard')
        
        except User.DoesNotExist:
            return render(request, 'mitrr/login.html', {'error': "Invalid username or password"})
    else:
        return render(request, 'mitrr/login.html')
    
def dashboard(request):
    user = request.session.get('userdata') 
    return render(request, 'mitrr/dashboard.html')

def teacher(request):
    jwttoken = request.session.get('jwttoken')
    url = "http://127.0.0.1:8000/" + "api/mitrr/teachers/"
    headers = {
        "Authorization": f"Bearer {jwttoken}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    context = {
        'teachers': response.json(),
    }
    return render(request, 'mitrr/teacher.html', context)

def student(request):
    jwttoken = request.session.get('jwttoken')
    url = "http://127.0.0.1:8000/" + "api/mitrr/students/"
    headers = {
        "Authorization": f"Bearer {jwttoken}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    context = {
        'students': response.json(),
    }
    return render(request, 'mitrr/student.html', context)

# rest
def add_teacher(request):
    jwttoken = request.session.get('jwttoken')
    if request.method == 'POST': 
        data = json.loads(request.body)
        teacherId = str(random.randint(10000, 99999))
        dataa = {
            "teacher_id": teacherId,
            "name": data['name'],
            "subjects": data['subject'],
            "email_id": data['email'],
            "phone_number": data['phone_number'],
            "password": data['name'][:3] + teacherId + '@jims',
        }
        
        url = "http://127.0.0.1:8000/" + "api/mitrr/teachers/add/"
        headers = {
            "Authorization": f"Bearer {jwttoken}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(dataa))
        if response.status_code == 200:
            return JsonResponse({'message': 'Success', 'data': response.json(), 'status': 200})
        if response.status_code == 400:
            return JsonResponse({'message': 'Error', 'data': response.json(), 'status': 400})

# REST API endpoint for adding a student
def add_student(request):
    jwttoken = request.session.get('jwttoken')
    if request.method == 'POST': 
        data = json.loads(request.body)
        enroll_number = str(random.randint(10000, 99999))
        student_data = {
            "enroll_number": enroll_number,
            "name": data['name'],
            "section": data['section'],
            "sem": data['sem'],
            "year": data['year'],
            "email_id": data['email'],
            "phone_number": data['phone_number'],
            "password": data['name'][:3] + enroll_number + '@jims',
        }
        
        url = "http://127.0.0.1:8000/" + "api/mitrr/students/add/"
        headers = {
            "Authorization": f"Bearer {jwttoken}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(student_data))
        if response.status_code == 200:
            return JsonResponse({'message': 'Success', 'data': response.json(), 'status': 200})
        if response.status_code == 400:
            return JsonResponse({'message': 'Error', 'data': response.json(), 'status': 400})

