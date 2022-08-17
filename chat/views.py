from django.shortcuts import redirect, render
from core.models import HelpCandidates, User, HELP_STATUS, Helper, OldPerson, Help
from .models import Chat
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required
def contacts(request):
    current_user = get_current_user(request)
    if current_user.isHelper:
        helper = get_helper_by_id(current_user.id)
        persons = OldPerson.objects.filter(id__in=Help.objects.filter(helper = helper).values("oldPerson"))
        contacts = User.objects.filter(id__in = persons.values("user"))
        for c in contacts:
            old_user = User.objects.filter(email = c).first()
            old_person = OldPerson.objects.filter(user = old_user).first()
            c.helps = Help.objects.filter(helper = helper, oldPerson = old_person)
    else:
        old_person = get_old_person_by_id(current_user.id)
        persons = Helper.objects.filter(id__in = Help.objects.filter(oldPerson = old_person, helper__isnull=False).values("helper"))
        contacts = User.objects.filter(id__in = persons.values("user"))
        for c in contacts:
            helper_user = User.objects.filter(email = c).first()
            helper = Helper.objects.filter(user = helper_user).first()
            c.helps = Help.objects.filter(oldPerson = old_person, helper = helper)
    return render(request, 'chat/contacts.html', {'contacts': contacts})

@login_required
def chat(request, id):
    print("current id is ", id)
    try:
        chat = Chat.objects.get(id=id)
    
        current_user = get_current_user(request)
        chat.receiver_user = get_receiver_user(current_user, chat.users.all())

        return render(request, 'chat/chat.html', {'chat': chat})
    except Chat.DoesNotExist:
        print("Chat no encontrado " +id)
        return redirect('chat:contacts')

def get_receiver_user(current_user, users):
    for u in users:
        if u.id != current_user.id:
            return u
    return "User not available"

def get_current_user(request):
    return User.objects.filter(email = request.user)[0]

def get_old_person_by_id(id):
    return OldPerson.objects.get(user_id = id)

def get_helper_by_id(id):
    return Helper.objects.get(user_id = id)