from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('home')

    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})