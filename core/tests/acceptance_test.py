import datetime
from django.test import Client, TestCase
from django.urls import reverse
from core.models import Help, HelpCandidates
from authentication.models import User
from core.models import Help, Helper, OldPerson
import random

class CoreAcceptanceTest(TestCase):
    def setUp(self):
        populate_users()
        populate_old_persons()
        populate_helpers()
        login(self)
        populate_help()
        populate_help_candidate()

    #As an Old person, I want to be able to create a request for help by describing my problem
    def test_use_case_create_help_request(self):
        self = login_as_old_person(self)
        oldPerson = OldPerson.objects.get(user_id = self.user.id)
        help_counter = Help.objects.all().count()
        help = Help.objects.create(description= "I want a friend to go to social events", category= "SO", oldPerson = oldPerson)
        help_counter_after_add = Help.objects.all().count()

        #Help request was created
        self.assertGreater(help_counter_after_add, help_counter)
        url = reverse('core:helpRequests')
        response = self.client.get(url)
        #Help is added to the list of help requests
        self.assertContains(response, help.description)

    #As an Old person, I want to be able to edit my help request
    def test_use_case_edit_help_request(self):
        self = login_as_old_person(self)
        oldPerson = OldPerson.objects.get(user_id = self.user.id)
        help = Help.objects.filter(oldPerson = oldPerson)[0]
        newDescription = "New description"
        help.description = newDescription
        help.save()
        url = reverse('core:helpRequests')
        response = self.client.get(url)
        #Help is modified in the list of help requests
        self.assertContains(response, newDescription)

    #As an Old person, I want to be able to delete help requests
    def test_use_case_delete_help_request(self):
        self = login_as_old_person(self)
        oldPerson = OldPerson.objects.get(user_id = self.user.id)
        help = Help.objects.filter(oldPerson = oldPerson).first()
        newDescription = "Description to be deleted"
        help.description = newDescription
        help.save()
        help.delete()
        url = reverse('core:helpRequests')
        response = self.client.get(url)
        #Help is deleted from the list of help requests
        self.assertNotContains(response, newDescription)

    #As an Old person, I want to be able to see the help requests previously submitted by me
    def test_use_case_see_my_help_requests(self):
        self = login_as_old_person(self)
        oldPerson = OldPerson.objects.get(user_id = self.user.id)
        helps = Help.objects.filter(oldPerson = oldPerson)
        url = reverse('core:helpRequests')
        response = self.client.get(url)
        for h in helps:
            self.assertContains(response, h.description)

    #As an Old person, I want to be able accept a help offer
    def test_use_case_accept_help_offer(self):
        self = login_as_old_person(self)
        oldPerson = OldPerson.objects.get(user_id = self.user.id)
        help = Help.objects.filter(oldPerson = oldPerson).first()
        candidate = HelpCandidates.objects.create(help = help, helper=help.helper, description="That sounds great, I can help be you")
        canditateInitialStatus = candidate.status
        accepted = next(
            (item for item in HELP_STATUS if item[1] == 'Accepted'),
            {}
        )
        candidate.status = accepted[0]
        candidate.save()
        #Help candidate status changes
        self.assertNotEqual(canditateInitialStatus, candidate.status)
        #The test to verify a new contact is added, corresponds to the Chat App

    #As an Old person, I want to be able to reject a help offer
    def test_use_case_reject_help_offer(self):
        self = login_as_old_person(self)
        oldPerson = OldPerson.objects.get(user_id = self.user.id)
        help = Help.objects.filter(oldPerson = oldPerson).first()
        candidate = HelpCandidates.objects.filter(help = help)[0]
        canditateInitialStatus = candidate.status
        rejected = next(
            (item for item in HELP_STATUS if item[1] == 'Rejected'),
            {}
        )
        candidate.status = rejected[0]
        candidate.save()
        #Help candidate status changes
        self.assertNotEqual(canditateInitialStatus, candidate.status)

    #As an Old person, I want to be able to see help offers from helpers
    def test_use_case_see_help_offers(self):
        self = login_as_old_person(self)
        oldPerson = OldPerson.objects.get(user_id = self.user.id)
        help = Help.objects.filter(oldPerson = oldPerson).first()
        candidates = HelpCandidates.objects.filter(help = help)
        url = reverse('core:getCandidates', args=(help.id,))
        response = self.client.get(url)      
        for c in candidates:
            #contains all the candidates
            self.assertContains(response, c.helper.user.name)

    
    #As a Helper, I want to be able to create a help offer
    def test_use_case_create_help_offer_to_request(self):
        helper = Helper.objects.get(user_id = self.user.id)
        help = Help.objects.first()
        newDescription = "Description of new help request"
        HelpCandidates.objects.filter(help = help, helper=helper).delete()
        help_candidate_counter = HelpCandidates.objects.all().count()
        candidature = HelpCandidates.objects.create(help = help, helper=helper, description=newDescription)
        candidature.description = newDescription
        candidature.save()
        help_candidate_counter_after_add = HelpCandidates.objects.all().count()

        #Help candidate was created
        self.assertGreater(help_candidate_counter_after_add, help_candidate_counter)
        url = reverse('core:myOffers')
        response = self.client.get(url)
        #Help candidature is added to the list
        self.assertContains(response, newDescription)
    
    #As a Helper, I want to be able to edit my help offers
    def test_use_case_edit_help_offer(self):
        helper = Helper.objects.get(user_id = self.user.id)
        candidature = HelpCandidates.objects.filter(helper=helper)[0]
        newDescription = "New candidate description"
        candidature.description = newDescription
        candidature.save()
        url = reverse('core:myOffers')
        response = self.client.get(url)
        #Help candidate is modified in the list
        self.assertContains(response, newDescription)
    
    #As a Helper, I want to be able to delete my help offers
    def test_use_case_delete_help_offer(self):
        helper = Helper.objects.get(user_id = self.user.id)
        candidature = HelpCandidates.objects.filter(helper=helper)[0]
        newDescription = "Description to be deleted"
        candidature.description = newDescription
        candidature.save()
        candidature.delete()
        url = reverse('core:myOffers')
        response = self.client.get(url)
        #Help candidate is deleted from the list of help requests
        self.assertNotContains(response, newDescription)

    #As a Helper, I want to be able to see my help offers
    def test_use_case_see_helpers_help_offers(self):
        helper = Helper.objects.get(user_id = self.user.id)
        candidatures = HelpCandidates.objects.filter(helper=helper)
        url = reverse('core:myOffers')
        response = self.client.get(url)
        for c in candidatures:
            self.assertContains(response, c.description)
        
    #As a Helper, I want to be able to see old persons’ help requests
    def test_use_case_see_help_requests(self):
        helps = Help.objects.filter(helper__isnull = True)
        url = reverse('core:myOffers')
        response = self.client.get(url)
        for h in helps:
            self.assertContains(response, h.description)

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
    return Help.objects.get_or_create(
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

def populate_help_candidate():
    help = Help.objects.first()
    HelpCandidates.objects.get_or_create(help = help, helper=help.helper, status='1', description="That sounds great, I can help be your company")[0]

HELP_STATUS = [
    ('1', 'Accepted'),
    ('2', 'Rejected'),
    ('3', 'In process'),
    ('4', 'Finished')
]