from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib.auth import authenticate, login as login_session, logout as logout_session
from django.contrib.auth.decorators import login_required
from django.apps import apps as django_apps


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
            login(request, user)

            return redirect('core:home')
    return render(request, 'authentication/signup.html', {'form': form})

def login(request):
    print("Login method")
    error_message = None
    if request.method == 'POST':
        print("POST")
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            login_session(request, user)
            print("Redirecting to home")
            return redirect('core:home')
        error_message = django_apps.get_app_config(
            'authentication').INVALID_CREDENTIALS_MESSAGE
    print("GET")
    return render(request, 'authentication/login.html', {"error_message": error_message})

@login_required()
def logout(request):
    logout_session(request)
    return redirect('core:home')
