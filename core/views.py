from django.shortcuts import render, redirect
from django.contrib.auth import login


# Create your views here.

def home(request):
    return render(request, 'core/home.html')

