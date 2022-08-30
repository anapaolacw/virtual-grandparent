import datetime
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from authentication.models import User
from core.models import Help, Helper, OldPerson
from chat.models import Chat

# Create your tests here.
class URLTests(TestCase):
    # Tests all urls
    def setUp(self):
        populate_users()
        login(self)
        populate_old_persons()
        populate_helpers()
        populate_help()
        populate_chat()

    def test_contacts_page(self):
        url = reverse('chat:contacts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_chat_page(self):
        chat = Chat.objects.first()
        url = reverse('chat:chat', args=(chat.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

def populate_users():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    users = [
        {
            "name": "Ana Paola Chazaro Watty",
            "email": "apcw96@gmail.com",
            "password": "123123",
            "phoneNumber": "07510302811",
            "dateOfBirth": dateOfBirth,
            "isHelper": True
        },
        {
            "name": "Samuel Jakobson",
            "email": "samuel@gmail.com",
            "password": "123123",
            "phoneNumber": "07510302811",
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

def populate_chat():
    help = Help.objects.first()
    chat = Chat.objects.create(isActive = True)
    chat.users.set([help.oldPerson.user, help.helper.user])

def login(self):
    self.client = Client()
    user = User.objects.first()
    self.user = user
    self.client.login(username=user.email, password="123123")