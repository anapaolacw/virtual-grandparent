from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from core.models import HelpCandidates, User, HELP_STATUS, Helper, OldPerson, Help
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
import datetime

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
        current_user = get_current_user(request)
        contact = User.objects.get(id=id)
        chat = Chat.objects.filter(users__in=[current_user, contact]).first()

        if not chat:
            chat = create_chat(current_user, contact)
        
        chat.receiver = contact
        chat.sender = current_user
        messages_format = get_messages_format(chat)
        return render(request, 'chat/chat.html', {'chat': chat, 'messages': messages_format})
    except Chat.DoesNotExist:
        print("Chat no encontrado ")
        return redirect('chat:contacts')

@login_required
def getMessages(request, id):
    chat = Chat.objects.get(id=id)
    messages_format = get_messages_format(chat)
    return JsonResponse({"messages": messages_format})

@login_required
def send(request):
    message = request.POST['message']
    chat_id = request.POST['chat_id']
    now = datetime.datetime.now()
    current_user = get_current_user(request)
    chat = Chat.objects.get(id=chat_id)
    new_message = Message.objects.create(type="txt", content=message, time=now, sender= current_user, chat = chat)
    new_message.save()
    return HttpResponse("Message sent successfully")

def get_messages_format(chat):
    messages = Message.objects.filter(chat=chat)
    messages_format = []
    for m in messages:
        m.senderName = m.sender.name
        messages_format.append({'content': m.content, 'time': m.time, 'senderName': m.sender.name})
    return messages_format

def create_chat(current_user, contact):
    slug = current_user.name.split('@')[0] + contact.name.split('@')[0]
    chat = Chat()
    chat.slug = slug
    print("slug " +slug)
    chat.save()
    chat.users.set([current_user, contact])
    chat.save()
    return chat

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