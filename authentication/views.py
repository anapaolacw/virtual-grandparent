from django.shortcuts import redirect, render
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login as login_session, logout as logout_session
from django.contrib.auth.decorators import login_required
from django.apps import apps as django_apps

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def signup(request):
    form = {}
    if(request.method == 'GET'):
        form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request)
            return redirect('core:home')
    return render(request, 'authentication/signup.html', {'form': form})

def login(request):
    error_message = None
    form = {}
    if request.method == 'GET':
        form = LoginForm()
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, email=email, password=password)
        if user and user.is_active:
            login_session(request, user)
            return redirect('core:home')
        error_message = django_apps.get_app_config(
            'authentication').INVALID_CREDENTIALS_MESSAGE
    return render(request, 'authentication/login.html', {'form': form, "error_message": error_message})

@login_required()
def logout(request):
    logout_session(request)
    return redirect('core:home')
