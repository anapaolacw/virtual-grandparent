from unicodedata import category
from django.shortcuts import render, redirect
from sqlalchemy import false, null, true
from tables import Description
from core.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Help, HelpCandidates, OldPerson, Helper, HELP_STATUS
from .forms import HelpRequestForm, HelpCandidateForm
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect


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
            return redirect('core:helpRequests')
        print(form.errors)
        error_message = form.errors
    return render(request, 'core/createHelpRequest.html', {'form': form, "error_message": error_message})

@login_required
@csrf_protect
def editHelpRequest(request, id):
    error_message = None
    form = {}
    help = Help.objects.get(pk = id)
    if request.method == 'GET':
        form = HelpRequestForm(instance=help)

    if request.method == 'POST':
        form = HelpRequestForm(request.POST)
        if form.is_valid():
            help.category = form.cleaned_data['category']
            help.description = form.cleaned_data['description']
            help.save()
            return redirect("core:helpRequests")
        print("ERRORS")
        print(form.errors)
        error_message = form.errors
    return render(request, 'core/editHelpRequest.html', {'id': help.id,'form': form, "error_message": error_message})

@login_required
def deleteHelpRequest(request, id):
    help = Help.objects.get(pk = id)
    help.delete()
    return redirect('core:helpRequests')

@login_required
def getCandidates(request, id):
    help = Help.objects.get(id = id)
    candidates = HelpCandidates.objects.filter(help = help)
    for c in candidates:
        print("Name:")
        c.helperName = c.helper.user.name
        print(c.helperName)
        print("Status")
        print(c.status)
    return render(request, 'core/candidates.html', {'candidates': candidates, 'help': help})


@login_required
def allHelpRequests(request):
    current_user = get_current_user(request)
    helper = get_helper_by_id(current_user.id)
    help_requests = Help.objects.filter(~Q(id__in=HelpCandidates.objects.all().values('help')))

    for h in help_requests:
        user = User.objects.get(email = h.oldPerson.user.email)
        h.oldPersonName = user.name

    isVerified = helper.isVerified
    return render(request, 'core/helpRequestList.html', {'help_requests': help_requests, 'isVerified': isVerified})

@login_required
def seeOffer(request, id):
    help = Help.objects.get(id = id)
    HelpCandidates.objects.get(help = help).delete()
    return redirect('core:allHelpRequests')    

@login_required
def myOffers(request):
    current_user = get_current_user(request)
    helper = get_helper_by_id(current_user.id)
    help_requests = Help.objects.filter(id__in=HelpCandidates.objects.filter(helper = helper).values('help'))
    for h in help_requests:
        user = User.objects.get(email = h.oldPerson.user.email)
        h.oldPersonName = user.name
        candidate = HelpCandidates.objects.filter(helper = helper, help = h).first()
        h.offerDescription = candidate.description
        h.status = candidate.get_status_display
    return render(request, 'core/myOffers.html', {'help_requests': help_requests})

@login_required
def deleteHelpOffer(request, id):
    current_user = get_current_user(request)
    helper = get_helper_by_id(current_user.id)
    help = Help.objects.get(id = id)
    helpCandidate = HelpCandidates.objects.filter(helper = helper, help = help)
    helpCandidate.delete()
    return redirect('core:myOffers')

@login_required
def rejectHelpOffer(request, id):
    helpCandidate = HelpCandidates.objects.get(id = id)
    inProgress = next(
        (item for item in HELP_STATUS if item[1] == 'Rejected'),
        {}
    )
    helpCandidate.status = inProgress[0]
    helpCandidate.save()
    return redirect('core:getCandidates', id=helpCandidate.help.id)

@login_required
def acceptHelpOffer(request, id):
    helpCandidate = HelpCandidates.objects.get(id = id)
    accepted = next(
        (item for item in HELP_STATUS if item[1] == 'Accepted'),
        {}
    )
    helpCandidate.status = accepted[0]
    helpCandidate.save()
    help = Help.objects.get(id = helpCandidate.help.id)
    help.helper = helpCandidate.helper
    help.save()
    return redirect('core:helpRequests')

@login_required
def createHelpOffer(request, id):
    error_message = None
    form = {}
    help_request = Help.objects.get(id= id)
    if request.method == 'GET':
        form = HelpCandidateForm()
        
    if request.method == 'POST':
        form = HelpCandidateForm(request.POST)
        if form.is_valid():
            current_user = get_current_user(request)
            helper = get_helper_by_id(current_user.id)
            HelpCandidates.objects.filter(helper = helper, help = help_request).delete()
            helpCandidate = form.save(commit=False)
            helpCandidate.helper = helper
            helpCandidate.help = help_request
            helpCandidate.save()
            return redirect('core:myOffers')
        print(form.errors)
        error_message = form.errors
    return render(request, 'core/createHelpOffer.html', {'form': form, "error_message": error_message,'help_request': help_request, 'id': id})

def editHelpOffer(request, id):
    current_user = get_current_user(request)
    helper = get_helper_by_id(current_user.id)
    error_message = None
    form = {}
    help = Help.objects.get(id = id)
    helpCandidate = HelpCandidates.objects.filter(helper = helper, help = help).first()
    print("Help candidate")
    print(helpCandidate)

    if request.method == 'GET':
        form = HelpCandidateForm(instance=helpCandidate)

    if request.method == 'POST':
        form = HelpCandidateForm(request.POST)
        if form.is_valid():
            helpCandidate.description = form.cleaned_data['description']
            print("New description: ")
            print(helpCandidate.description)
            helpCandidate.save()
            return redirect("core:myOffers")
        print("ERRORS")
        print(form.errors)
        error_message = form.errors
    return render(request, 'core/editHelpOffer.html', {'id': id,'form': form, "error_message": error_message, 'help_request': help})


def get_current_user(request):
    return User.objects.filter(email = request.user)[0]

def get_old_person_by_id(id):
    return OldPerson.objects.get(user_id = id)

def get_helper_by_id(id):
    return Helper.objects.get(user_id = id)