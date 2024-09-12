import requests , json , random
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from mitrr.models import User, CustomSession
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)

            # Delete any existing session for the user
            CustomSession.objects.filter(user=user).delete()

            # Create a new session
            customsession = CustomSession.objects.create(
                user=user,
                usertype='teacher',
                userdata={
                    'name': user.name,
                    'username': user.username,
                    'usertype': 'teacher',
                    'data':[]
                },
                created_at=timezone.now()
            )
            # store data in session
            request.session['jwttoken'] = str(customsession.jwttoken)
            request.session['userdata'] = str(customsession.userdata)

            return redirect('dashboard')
        
        except User.DoesNotExist:
            return render(request, 'teacher/login.html', {'error': "Invalid username or password"})
        
    else:
        return render(request, 'teacher/login.html')
    
def take_attendance(request):
    return render(request, 'teacher/addAttendance.html') 