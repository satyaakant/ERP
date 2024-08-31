import requests
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(requests):
    return HttpResponse("login student")

def dashboard(requests):    
    return HttpResponse("dashboard student")