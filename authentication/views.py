from django.shortcuts import redirect, render
from django.urls import reverse
from sqlalchemy import true

from core.models import Helper, OldPerson
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login as login_session, logout as logout_session
from django.contrib.auth.decorators import login_required
from django.apps import apps as django_apps

from django.contrib.auth import get_user_model
from django.http import HttpResponse
User = get_user_model()
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            isHelper = form.cleaned_data['isHelper']
            user.isHelper = isHelper
            user.save()
            if(isHelper):
                Helper.objects.create(user=user)
                login(request)
                return HttpResponse(reverse('core:helperMenu'))

            OldPerson.objects.create(user=user)
            login(request)
            return HttpResponse(reverse('core:menu'))

    form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form })

def login(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, email=email, password=password)
        if user and user.is_active:
            login_session(request, user)
            if(is_old_person(user.id)):
                return redirect('core:menu')
            return redirect('core:helperMenu')
        print("Error")
        error_message = django_apps.get_app_config(
            'authentication').INVALID_CREDENTIALS_MESSAGE
    form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form, "error_message": error_message})

@login_required()
def logout(request):
    logout_session(request)
    return redirect('core:home')

def is_old_person(id):
    return OldPerson.objects.filter(user_id = id).count() > 0