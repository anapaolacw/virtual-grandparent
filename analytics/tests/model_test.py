import datetime
from django.test import TestCase
from analytics.models import Transaction
from authentication.models import User
from core.models import Help, OldPerson
class AnalyticsModelTest(TestCase):
    def test_add_analytics(self):
        transaction_counter = Transaction.objects.all().count()
        old_person = add_old_person(add_user())
        help = add_help(old_person)
        Transaction.objects.get_or_create(
            emailUser1 = old_person.user.email, 
            model = "Help request", 
            action = "Created",
            details = "User "+str(old_person.user.name)+ "created a help request with id  "+str(help.id)+ "with the following description: "+help.description
        )
        transaction_counter_after_add = Transaction.objects.all().count()
        self.assertGreater(transaction_counter_after_add, transaction_counter)

def add_user():
    dateOfBirth = datetime.datetime(1996, 1, 27)
    user = {
        "name": "Ana Paola Chazaro Watty",
        "email": "apcw96@gmail.com",
        "password": "123123",
        "phoneNumber": "07510302811",
        "dateOfBirth": dateOfBirth,
        "isHelper": False
    }
    u = User.objects.get_or_create(name=user['name'], email = user['email'], phoneNumber = user['phoneNumber'], dateOfBirth=user['dateOfBirth'], isHelper=user['isHelper'])[0]
    u.set_password(user['password'])
    u.save()
    return u

def add_old_person(user):
    return OldPerson.objects.get_or_create(needsHelp = True, user = user)[0]

def add_help(old_person):
    return Help.objects.get_or_create(
        description= "I want a friend to go to social events in my community",
        category= "SO",
        oldPerson = old_person
    )[0]