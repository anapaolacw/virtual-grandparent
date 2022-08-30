import datetime
from django.test import Client, TestCase
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import null
from core.models import Help, HelpCandidates
from authentication.models import User
from core.models import Help, Helper, OldPerson
from chat.models import Chat
import random


class CoreModelsTest(TestCase):
    def setUp(self):
        populate_users()
        login(self)
    
    def test_add_old_person(self):
        old_persons_counter = OldPerson.objects.all().count()
        populate_old_persons()
        old_persons_counter_after_add = OldPerson.objects.all().count()
        self.assertGreater(old_persons_counter_after_add, old_persons_counter)

    def test_add_helper(self):
        helper_counter = Helper.objects.all().count()
        populate_helpers()
        helper_counter_after_add = Helper.objects.all().count()
        self.assertGreater(helper_counter_after_add, helper_counter)

    def test_add_help(self):
        help_counter = Help.objects.all().count()
        populate_old_persons()
        populate_helpers()
        populate_help()
        help_counter_after_add = Help.objects.all().count()
        self.assertGreater(help_counter_after_add, help_counter)

    def test_add_help_candidate(self):
        candidate_counter = HelpCandidates.objects.all().count()
        populate_old_persons()
        populate_helpers()
        populate_help()
        populate_help_candidates()
        candidate_counter_after_add = HelpCandidates.objects.all().count()
        self.assertGreater(candidate_counter_after_add, candidate_counter)

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

def populate_help_candidates():
    helpers = list(Helper.objects.all())
    helps = Help.objects.all()
    descriptions = ["I  have experience doing that", "I think I can be useful because I have experience", "I would like to help you out!", "That sounds great, I can help with that", "Count me in, I have a lot of free time recently", "Sounds lovely, It would be an honor to help you"]
    for h in helps:
        if(h.helper):
            HelpCandidates.objects.get_or_create(help = h, helper=h.helper, status='1', description=random.choice(descriptions))
        else:
            HelpCandidates.objects.get_or_create(help = h, helper=random.choice(helpers), status='3', description=random.choice(descriptions))

def login(self):
    self.client = Client()
    user = User.objects.first()
    self.user = user
    self.client.login(username=user.email, password="123123")


def login_as_old_person(self):
    self.client = Client()
    user = OldPerson.objects.first().user
    self.user = user
    self.client.login(username=user.email, password="123123")
    return self