import datetime
from django.test import Client, TestCase
from django.urls import reverse
from sqlalchemy import null
from authentication.models import User
from core.models import Helper, OldPerson

class AuthenticationAcceptanceTest(TestCase):
    # As a User, I want to be able to Login to the system  as old perosn
    def test_use_case_login_as_old_person(self):
        add_old_person_user()
        self = login_as_old_person(self)
        #After login, redirect to menu
        url = reverse('core:menu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    # As a User, I want to be able to Login to the system  as helper
    def test_use_case_login_as_helper(self):
        add_helper_user()
        self = login_as_helper(self)
        #After login, redirect to helper menu
        url = reverse('core:helperMenu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # As a User I want to be able to logout from the system
    def test_use_case_logout(self):
        add_helper_user()
        self = login_as_helper(self)
         # Log out
        self.client.logout()
        self.assertNotIn(self.client.session, ['_auth_user_id'])

    # As a User, I want to be able to register myself in the system as an old person or as a helper
    def test_use_case_signup(self):
        users_counter = User.objects.all().count()
        dateOfBirth = datetime.datetime(1996, 1, 27)
        user = {
            "name": "New user",
            "email": "new@gmail.com",
            "password": "123123",
            "phoneNumber": "07510302811",
            "dateOfBirth": dateOfBirth,
            "isHelper": True
        }
        u = User.objects.get_or_create(name=user['name'], email = user['email'], phoneNumber = user['phoneNumber'], dateOfBirth=user['dateOfBirth'], isHelper=user['isHelper'])[0]
        u.set_password(user['password'])
        u.save()
        users_counter_after_add = User.objects.all().count()
        self.assertGreater(users_counter_after_add, users_counter)

def login_as_helper(self):
    self.client = Client()
    user = Helper.objects.first().user
    self.user = user
    self.client.login(username=user.email, password="123123")
    return self

def login_as_old_person(self):
    self.client = Client()
    user = OldPerson.objects.first().user
    self.user = user
    self.client.login(username=user.email, password="123123")
    return self

def add_helper_user():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    user = {
        "name": "Ana Paola Chazaro Watty",
        "email": "apcw96@gmail.com",
        "password": "123123",
        "phoneNumber": "07510302811",
        "dateOfBirth": dateOfBirth,
        "isHelper": True
    }
    u = User.objects.get_or_create(name=user['name'], email = user['email'], phoneNumber = user['phoneNumber'], dateOfBirth=user['dateOfBirth'], isHelper=user['isHelper'])[0]
    u.set_password(user['password'])
    u.save()
    Helper.objects.get_or_create(user = u)

def add_old_person_user():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    user = {
        "name": "Ana Paola Chazaro Watty",
        "email": "apcw96@gmail.com",
        "password": "123123",
        "phoneNumber": "07510302811",
        "dateOfBirth": dateOfBirth,
        "isHelper": True
    }
    u = User.objects.get_or_create(name=user['name'], email = user['email'], phoneNumber = user['phoneNumber'], dateOfBirth=user['dateOfBirth'], isHelper=user['isHelper'])[0]
    u.set_password(user['password'])
    u.save()
    OldPerson.objects.get_or_create(user = u)

def add_manager():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    user = {
        "name": "admin",
        "email": "admin@gmail.com",
        "password": "123123",
        "phoneNumber": "07510302811",
        "dateOfBirth": dateOfBirth,
        "is_superuser": True,
        "is_staff": True
    }
    u = User.objects.get_or_create(name=user["name"], email = user['email'], phoneNumber = user['phoneNumber'], 
            dateOfBirth=user["dateOfBirth"], is_staff=user["is_staff"], is_superuser = user["is_superuser"])[0]
    u.set_password(user['password'])
    u.save()