import datetime
from django.test import Client, TestCase
from authentication.models import User
from core.models import Help, HelpCandidates, Helper, OldPerson
from chat.models import Chat
from django.urls import reverse

# Create your tests here.
class URLTests(TestCase):
    # Tests all urls
    def setUp(self):
        populate_users()
        populate_old_persons()
        populate_helpers()
        login(self)
        populate_help()
        populate_help_candidate()

    def test_home_page(self):
        url = reverse('core:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_helper_menu_page(self):
        url = reverse('core:helperMenu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_help_requests_page(self):
        self = login_as_old_person(self)
        url = reverse('core:helpRequests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_help_requests_page(self):
        url = reverse('core:allHelpRequests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_help_request_page(self):
        url = reverse('core:createHelpRequest')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_help_request_page(self):
        help = Help.objects.first()
        url = reverse('core:editHelpRequest', args=(help.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_help_request_page(self):
        self = login_as_old_person(self)
        help = Help.objects.first()
        url = reverse('core:deleteHelpRequest', args=(help.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('core:helpRequests'), 
            status_code=302, target_status_code=200, fetch_redirect_response=True)


    def test_create_help_offer_page(self):
        help = Help.objects.first()
        url = reverse('core:createHelpOffer', args=(help.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_help_request_candidates_page(self):
        help = Help.objects.first()
        url = reverse('core:getCandidates', args=(help.id,))
        response = self.client.get(url)
        url = reverse('core:getCandidates', args=(help.id,))        
        self.assertEqual(response.status_code, 200)

    def test_reject_candidate_page(self):
        self = login_as_old_person(self)
        c = HelpCandidates.objects.first()
        url = reverse('core:rejectHelpOffer', args=(c.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('core:getCandidates', args=(c.help.id,)), 
            status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_accept_candidate_page(self):
        self = login_as_old_person(self)
        c = HelpCandidates.objects.first()
        url = reverse('core:acceptHelpOffer', args=(c.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('core:helpRequests'), 
            status_code=302, target_status_code=200, fetch_redirect_response=True)


    def test_delete_offer_page(self):
        help = Help.objects.first()
        url = reverse('core:deleteHelpOffer', args=(help.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('core:myOffers'), 
            status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_edit_offer_page(self):
        help = Help.objects.first()
        url = reverse('core:editHelpOffer', args=(help.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_offers_page(self):
        help = Help.objects.first()
        url = reverse('core:seeOffer', args=(help.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('core:allHelpRequests'), 
            status_code=302, target_status_code=200, fetch_redirect_response=True)


    def test_my_offers_page(self):
        url = reverse('core:myOffers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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

def login(self):
    self.client = Client()
    user = Helper.objects.first().user
    self.user = user
    self.client.login(username=user.email, password="123123")

def login_as_old_person(self):
    self.client = Client()
    user = OldPerson.objects.first().user
    self.user = user
    self.client.login(username=user.email, password="123123")
    return self

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

def populate_help_candidate():
    help = Help.objects.first()
    HelpCandidates.objects.get_or_create(help = help, helper=help.helper, status='1', description="That sounds great, I can help be your company")[0]
