from django.test import TestCase
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import null
from core.models import Help

class TestAppModels(TestCase):
    def test_model_str(self):
        description = Help.objects.create(description="I would like to get help to transport myself",
        category= 'TR', helper = null, oldPerson = null)
        self.assertEquals(str(description), "I would like to get help to transport myself")
