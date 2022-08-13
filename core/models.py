from django.db import models
from django.contrib.auth import get_user_model as user_model
from sqlalchemy import true
User = user_model()

HELP_CATEGORIES = [
    (None, '----------'),
    ('HA', 'Handyperson services'),
    ('HO', 'Home visiting'),
    ('PH', 'Phone calls/Chatting'),
    ('SO', 'Social activities'),
    ('TE', 'Technology issues'),
    ('TR', 'Transportation'),
    ('OT', 'Others')
]

HELP_STATUS = [
    ('1', 'Active'),
    ('2', 'Rejected'),
    ('3', 'In process'),
    ('4', 'Finished')
]
class OldPerson(models.Model):
    needsHelp: models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Helper(models.Model):
    isAproved: models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Help(models.Model):
    status: models.CharField(max_length=1, choices = HELP_STATUS, default='1') #status can be 1: active, 2: rejected, 3: in progress, 4: finished
    description = models.TextField(max_length=1000)
    category = models.CharField(choices=HELP_CATEGORIES, max_length=2, default='OT')
    helper = models.ForeignKey(Helper, on_delete=models.CASCADE, null=True)
    oldPerson = models.ForeignKey(OldPerson, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

