import datetime
from django.test import TestCase
from sqlalchemy import null
from authentication.models import User

class AuthenticationModelTest(TestCase):
    def test_add_user(self):
        users_counter = User.objects.all().count()
        add_user()
        users_counter_after_add = User.objects.all().count()
        self.assertGreater(users_counter_after_add, users_counter)

    def test_add_manager_user(self):
        users_counter = User.objects.filter(is_superuser = True).count()
        add_manager()
        users_counter_after_add = User.objects.filter(is_superuser = True).count()
        self.assertGreater(users_counter_after_add, users_counter)

    def test_add_existing_user(self):
        add_user()
        users_counter = User.objects.filter().count()
        add_user()
        users_counter_after_add = User.objects.all().count()
        self.assertEqual(users_counter_after_add, users_counter)

def add_user():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    user = {
        "name": "Ana Paola Chazaro Watty",
        "email": "apcw96@gmail.com",
        "password": "123123",
        "phoneNumber": "7510302811",
        "dateOfBirth": dateOfBirth,
        "isHelper": True
    }
    u = User.objects.get_or_create(name=user['name'], email = user['email'], phoneNumber = user['phoneNumber'], dateOfBirth=user['dateOfBirth'], isHelper=user['isHelper'])[0]
    u.set_password(user['password'])
    u.save()

def add_manager():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    user = {
        "name": "admin",
        "email": "admin@gmail.com",
        "password": "123123",
        "phoneNumber": "7510302811",
        "dateOfBirth": dateOfBirth,
        "is_superuser": True,
        "is_staff": True
    }
    u = User.objects.get_or_create(name=user["name"], email = user['email'], phoneNumber = user['phoneNumber'], 
            dateOfBirth=user["dateOfBirth"], is_staff=user["is_staff"], is_superuser = user["is_superuser"])[0]
    u.set_password(user['password'])
    u.save()