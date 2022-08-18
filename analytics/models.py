from django.db import models
from django.utils.timezone import now

# Create your models here.
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    emailUser1 = models.EmailField(max_length=200)
    emailUser2 = models.EmailField(max_length=200, blank=True)
    dateTime = models.DateTimeField(default=now)
    model = models.CharField(max_length=200, blank=True)
    action = models.CharField(max_length=250)
    details = models.TextField(max_length=1000, blank=True)