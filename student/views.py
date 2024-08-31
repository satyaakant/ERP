from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return HttpResponse("login student")

def dashboard(request):    
    return HttpResponse("dashboard student")