from django.shortcuts import redirect, render
from core.models import User
from .models import Chat
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required
def contacts(request):
    current_user = get_current_user(request)
    user_chats = Chat.objects.filter(users__email = current_user.email)

    for c in user_chats:
        c.receiver_user = get_receiver_user(current_user, c.users.all())

    return render(request, 'chat/contacts.html', {'chats': user_chats})

@login_required
def chat(request, slug):
    print("current slug is ", slug)
    try:
        chat = Chat.objects.get(slug=slug)
    
        current_user = get_current_user(request)
        chat.receiver_user = get_receiver_user(current_user, chat.users.all())

        return render(request, 'chat/chat.html', {'chat': chat})
    except Chat.DoesNotExist:
        print("Chat no encontrado " +slug)
        return redirect('chat:contacts')

def get_receiver_user(current_user, users):
    for u in users:
        if u.id != current_user.id:
            return u
    return "User not available"

def get_current_user(request):
    return User.objects.filter(email = request.user)[0]