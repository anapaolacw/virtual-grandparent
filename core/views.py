from unicodedata import category
from django.shortcuts import render, redirect
from tables import Description
from core.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Help, HelpCandidates, OldPerson
from .forms import HelpRequestForm


# Create your views here.

def home(request):
    return render(request, 'core/home.html')

@login_required
def oldMenu(request):
    return render(request, 'core/oldMenu.html')

@login_required
def helperMenu(request):
    return render(request, 'core/helperMenu.html')

@login_required
def helpRequests(request):
    current_user = get_current_user(request)
    old_person = get_old_person_by_id(current_user.id)
    help_requests = Help.objects.filter(oldPerson = old_person)
    for h in help_requests:
        h.candidates = HelpCandidates.objects.filter(help = h)

    return render(request, 'core/helpRequests.html', {'help_requests': help_requests})

@login_required
def createHelpRequest(request):
    error_message = None
    form = {}
    if request.method == 'GET':
        form = HelpRequestForm()
        
    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            help = form.save(commit=False)
            help.oldPerson = get_old_person_by_id(get_current_user(request).id)
            help.save()
            messages.info(request, 'Your password has been changed successfully!')
            return redirect('core:helpRequests')
        print(form.errors)
        error_message = form.errors
    return render(request, 'core/createHelpRequest.html', {'form': form, "error_message": error_message})

@login_required
def editHelpRequest(request, id):
    error_message = None
    form = {}
    help = Help.objects.get(pk = id)
    if request.method == 'GET':
        print("getting form")
        form = HelpRequestForm(instance=help)

    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            help.category = form.cleaned_data['category']
            help.description = form.cleaned_data['description']
            help.save()
            messages.info(request, 'Your password has been changed successfully!')
            return redirect('core:helpRequests')
        print(form.errors)
        error_message = form.errors
    return render(request, 'core/editHelpRequest.html', {'id': help.id,'form': form, "error_message": error_message})

@login_required
def deleteHelpRequest(request, id):
    help = Help.objects.get(pk = id)
    help.delete()
    return redirect('core:helpRequests')

def get_current_user(request):
    return User.objects.filter(email = request.user)[0]

def get_old_person_by_id(id):
    return OldPerson.objects.get(user_id = id)