from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.apps import apps as django_apps
from sqlalchemy import true

class Manager(BaseUserManager):
    def create_user(self, name, email, password, phoneNumber, dateOfBirth, **kwargs):
        if not email:
            raise ValueError('User must have a email address')
        user = self.model(email=self.normalize_email(
            email), username = email, name = name, phoneNumber=phoneNumber, dateOfBirth = dateOfBirth, **kwargs)
        if not password:
            raise ValueError('User must have a password field')
        user.save()
        user.set_password(password)

        return user

    def create_superuser(self, name, email, password, phoneNumber, dateOfBirth, **kwargs):
        user = self.create_user(
            name, email, password, phoneNumber, dateOfBirth)
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
    dateOfBirth = models.DateField(null=true)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = Manager()
    class Meta:
        unique_together = ('email',)
