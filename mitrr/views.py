from django.utils import timezone
from django.shortcuts import render, redirect
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
            session = CustomSession.objects.create(
                user=user,
                usertype='mitrr',
                userdata={'key': 'value'},
                created_at=timezone.now()
            )

            # Redirect to the dashboard after login
            return redirect('dashboard/')
        
        except User.DoesNotExist:
            return render(request, 'mitrr/login.html', {'error': "Invalid username or password"})
    else:
        return render(request, 'mitrr/login.html')
    
def dashboard(request):
    return render(request, 'mitrr/dashboard.html')

def teacher(request):
    return render(request, 'mitrr/teacher.html')

def student(request):
    return render(request, 'mitrr/student.html')


