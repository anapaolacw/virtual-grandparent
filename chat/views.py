from django.shortcuts import render
from core.models import User
from .models import Chat
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def chats(request):
    print("Request")
    print(request.user)
    for p in User.objects.all():
        print(p)
    # current_person = Person.objects.get(user = request.user)
    # print("Current person")
    # print(current_person)
    # chats = Chat.objects.filter(participants = current_person)
    # print("CHATS")
    # for chat in chats:
    #     print(chat.id)
    #     print(chat.isActive)
    #     print(chat.slug)
    #     print(chat.participants.all())


    return render(request, 'chat/chats.html', {'chats': chats})