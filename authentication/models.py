from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.apps import apps as django_apps

class Manager(BaseUserManager):
    def create_user(self, name, age, phoneNumber, email, password, **kwargs):
        if not email:
            raise ValueError('User must have a email address')
        user = self.model(email=self.normalize_email(
            email), username = email, name = name, age=age, phoneNumber=phoneNumber, **kwargs)
        if not password:
            raise ValueError('User must have a password field')
        user.save()
        user.set_password(password)

        return user

    def create_superuser(self, name, age, phoneNumber, email, password, **kwargs):
        user = self.create_user(
            name, age, phoneNumber, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractUser):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=200)
    isHelper = models.BooleanField(default=True)
    age = models.SmallIntegerField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = Manager()
    class Meta:
        unique_together = ('email',)
