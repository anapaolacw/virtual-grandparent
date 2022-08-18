import datetime
from django.test import Client, TestCase
from sqlalchemy import null
from chat.models import Chat, Message, Call
from authentication.models import User
from core.models import Help, Helper, OldPerson
from chat.models import Chat

class ChatModelsTest(TestCase):
    def setUp(self):
        populate_users()
        login(self)
        populate_old_persons()
        populate_helpers()
        populate_help()

    def test_create_chat(self):
        help = Help.objects.first()
        chats_counter = Chat.objects.all().count()
        Chat.objects.create(isActive = True)
        chats_counter_after_add = Chat.objects.all().count()
        self.assertGreater(chats_counter_after_add, chats_counter)

    def test_create_chat_with_users(self):
        help = Help.objects.first()
        chat = Chat.objects.create(isActive = True)
        chat.users.set([help.oldPerson.user, help.helper.user])
        self.assertEqual(chat.users.count(), 2)

    def test_create_message(self):
        help = Help.objects.first()
        chat = Chat.objects.create(isActive = True)
        chat.users.set([help.oldPerson.user, help.helper.user])
        messages_counter = Message.objects.all().count()
        Message.objects.create(
            type= "txt",
            content= "Hello, nice to meet you!",
            sender= chat.users.filter(isHelper = True)[0],
            chat= chat,
        )
        messages_counter_after_add = Message.objects.all().count()
        self.assertGreater(messages_counter_after_add, messages_counter)
    
    
def populate_users():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    users = [
        {
            "name": "Ana Paola Chazaro Watty",
            "email": "apcw96@gmail.com",
            "password": "123123",
            "phoneNumber": "7510302811",
            "dateOfBirth": dateOfBirth,
            "isHelper": True
        },
        {
            "name": "Samuel Jakobson",
            "email": "samuel@gmail.com",
            "password": "123123",
            "phoneNumber": "7510302811",
            "dateOfBirth": dateOfBirth,
            "isHelper": False
        },
    ]
    for user in users:
        u = User.objects.get_or_create(name=user['name'], email = user['email'], phoneNumber = user['phoneNumber'], dateOfBirth=user['dateOfBirth'], isHelper=user['isHelper'])[0]
        u.set_password(user['password'])
        u.save()

def populate_old_persons():
    old_users = User.objects.filter(isHelper = False)

    for u in old_users:
        OldPerson.objects.get_or_create(needsHelp = True, user = u)

def populate_helpers():
    helpers = User.objects.filter(isHelper = True)

    for u in helpers:
        Helper.objects.get_or_create(user = u)

def populate_help():
    old_person = OldPerson.objects.first()
    helper = Helper.objects.first()
    Help.objects.get_or_create(
        description= "I want a friend to go to social events in my community",
        category= "SO",
        oldPerson = old_person,
        helper = helper
    )

def login(self):
    self.client = Client()
    user = User.objects.first()
    self.user = user
    self.client.login(username=user.email, password="123123")