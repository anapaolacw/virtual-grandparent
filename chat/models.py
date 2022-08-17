from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now
from django.contrib.auth import get_user_model as user_model
User = user_model()

# Create your models here.
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    isActive = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True)
    users = models.ManyToManyField(User)

class Message(models.Model):
    type = models.CharField(max_length=10) #1: text, 2: image
    content = models.TextField(max_length=1000, null=False)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    time = models.DateTimeField(default=now, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

class Call(models.Model):
    type = models.CharField(max_length=10) #1: call, 2: videocall
    time = models.DateTimeField(default=now, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
