import datetime
from django.test import TestCase
from sqlalchemy import null
from chat.models import Chat, Message, Call
from authentication.models import User

class TestAppModels(TestCase):
    def test_model_str(self):
        chat = Chat.objects.create(isActive = True)
        self.assertEquals(chat.id, 1)

    def test_users_in_chat(self):
        now = datetime.datetime.now()
        testUser = User.objects.create_user(name = "User name", email="email@gmail.com", password = "password", phoneNumber="12345678", isHelper=True, dateOfBirth=now)
        testUser2 = User.objects.create_user(name = "User name", email="email2@gmail.com", password = "password", phoneNumber="12345678", isHelper=True, dateOfBirth=now)
        chat = Chat.objects.create(isActive = True)
        chat.users.set([testUser, testUser2])
        self.assertEqual(chat.users.count(), 2)
    
    