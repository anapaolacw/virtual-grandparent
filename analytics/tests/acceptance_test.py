import datetime
from django.test import TestCase
from analytics.models import Transaction
from authentication.models import User
from django.urls import reverse
from django.test import Client
from core.models import Help, Helper, OldPerson, HelpCandidates
from populate import populate_transactions
import random

class AnalyticsAcceptanceTest(TestCase):
    def setUp(self):
        populate_users()
        populate_old_persons()
        populate_helpers()
        populate_helps()
        
    #As a Manager, I want to be able to see a record of transactions
    def test_use_case_get_transactions(self):
        transaction_counter = Transaction.objects.all().count()
        user = User.objects.first()
        Transaction.objects.get_or_create(
            emailUser1 = user.email, 
            model = "Help request", 
            action = "Created",
            details = "New transaction is added"
        )
        transaction_counter_after_add = Transaction.objects.all().count()
        #add a transaction
        self.assertGreater(transaction_counter_after_add, transaction_counter)

        populate_transactions()
        transactions = Transaction.objects.all()
        url = reverse('analytics:transactions')
        response = self.client.get(url)
        #get all transactions
        for t in transactions:
            self.assertContains(response, t.details)

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
    helper_users = User.objects.filter(isHelper = True)

    for u in helper_users:
        Helper.objects.get_or_create(isVerified = True, user = u)

def populate_helps():
    d1 = datetime.datetime(2022, 8, 8)
    d2 = datetime.datetime(2022, 9, 2)
    helpers = list(Helper.objects.all())
    oldPersons = list(OldPerson.objects.all())
    helps_with_helper = [
        {
            "description": "Hello, I would like to have a phone buddy to call when I feel lonely",
            "category": "PH",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I want company to go to the church on sundays",
            "category": "SO",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "Hello, I would like to learn how to create zoom meetings with my friends. Cheers",
            "category": "TE",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "Hello. I would like to have someone to talk to. I am a very talkative person but don't have many friends",
            "category": "HO",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I would appreciate if someone helped me out moving some old boxed that I have",
            "category": "TR",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I want a friend to go for a walk in the mornings",
            "category": "SO",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I would appreciate some company on week days because I get bored",
            "category": "HO",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I want to go to the market outside the city but I don't have car, could someone please help me?",
            "category": "TR",
            "helper": random.choice(helpers),
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        }
    ]
    helps_without_helper = [
        {
            "description": "I would appreciate having help for painting my walls because they are very dirty",
            "category": "HA",
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I am looking for someone who want to go to museums with me",
            "category": "SO",
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I would like someone to take me places because I can't see anymore and I don't want to stay at home every day",
            "category": "TR",
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I would like to meet someone who is interested on plants and flowers to help me with my garden",
            "category": "OT",
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I want to learn how to use facebook",
            "category": "TE",
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "I want a friend to go to social events in my community",
            "category": "SO",
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        {
            "description": "My printer doesn't work and I don't know who to ask",
            "category": "TE",
            "oldPerson": random.choice(oldPersons),
            "date": random_date(d1, d2),
        },
        
    ]
    for h in helps_with_helper:
        Help.objects.get_or_create(description= h['description'], category=h['category'], helper = h['helper'], oldPerson = h['oldPerson'], date = h['date'])

    for h in helps_without_helper:
        Help.objects.get_or_create(description= h['description'], category=h['category'], oldPerson = h['oldPerson'], date = h['date'])

def populate_help_candidates():
    helpers = list(Helper.objects.all())
    helps = Help.objects.all()
    descriptions = ["I  have experience doing that", "I think I can be useful because I have experience", "I would like to help you out!", "That sounds great, I can help with that", "Count me in, I have a lot of free time recently", "Sounds lovely, It would be an honor to help you"]
    for h in helps:
        if(h.helper):
            HelpCandidates.objects.get_or_create(help = h, helper=h.helper, status='1', description=random.choice(descriptions))
        else:
            HelpCandidates.objects.get_or_create(help = h, helper=random.choice(helpers), status='3', description=random.choice(descriptions))

def populate_transactions():
    helps = Help.objects.all()
    transactions = []
    for h in helps:
        transactions.append({
            "emailUser1": h.oldPerson.user.email, 
            "model": "Help request", 
            "action": "Created",
            "details": "User "+str(h.oldPerson.user.name)+" created a help request with id " +str(h.id)+" with the following description: "+h.description
        })
    for t in transactions:
        Transaction.objects.get_or_create(emailUser1= t['emailUser1'], model=t['model'], action=t['action'], details=t['details'])

    transactions = []
    candidates = HelpCandidates.objects.all()
    for c in candidates:
        transactions.append({
                "emailUser1": c.helper.user.email, 
                "emailUser2": c.help.oldPerson.user.email,
                "model": "Help offer", 
                "action": "Created",
                "details": "User "+c.helper.user.name+" created a help offer with id "+str(h.id)+" with the following description: "+h.description
            })
        if c.status == '1':
            transactions.append({
                "emailUser1": c.help.oldPerson.user.email, 
                "emailUser2": c.helper.user.email,
                "model": "Help offer", 
                "action": "Accepted",
                "details": "User "+c.help.oldPerson.user.email+" accepted a help offer with id "+str(c.id)+" offered by: "+c.helper.user.email
            })
    for t in transactions:
        Transaction.objects.get_or_create(emailUser1= t['emailUser1'], emailUser2 = t['emailUser2'], model=t['model'], action=t['action'], details=t['details'])

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)
