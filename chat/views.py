from django.shortcuts import render
from core.models import User
from .models import Chat
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required
def chats(request):
    current_user = get_current_user(request)
    user_chats = Chat.objects.filter(users__email = current_user.email)

    for c in user_chats:
        c.receiver_user = get_receiver_user(current_user, c.users.all())
        print("Receiver user: ")
        print(c.receiver_user)

    return render(request, 'chat/chats.html', {'chats': user_chats})

@login_required
def chat(request, slug):
    chat = Chat.objects.get(slug=slug)
    current_user = get_current_user(request)
    chat.receiver_user = get_receiver_user(current_user, chat.users.all())
    print("Receiver user: ", chat.receiver_user)

    return render(request, 'chat/chat.html', {'chat': chat})

def get_receiver_user(current_user, users):
    for u in users:
        print("current user ")
        print(current_user)
        print("current id is ")
        print(current_user.id)
        print("comparing to id")
        print(u.id)
        if u.id != current_user.id:
            return u
    return "User not available"

def get_current_user(request):
    return User.objects.filter(email = request.user)[0]