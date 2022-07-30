from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.apps import apps as django_apps

class Manager(BaseUserManager):
    def create_user(self, name, age, phoneNumber, email, password, type, **kwargs):
        if not email:
            raise ValueError('User must have a email address')
        user = self.model(email=self.normalize_email(
            email), username=username, type=type, **kwargs)
        if type == django_apps.get_app_config('core').type['PASSWORD_LOGIN']:
            if not password:
                raise ValueError('User must have a password field')
            user.save()
            user.set_password(password)
        else:
            user.save()
        
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(
            email,
            password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractUser):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    REQUIRED_FIELDS = ['email', 'name', 'password', 'age', 'phoneNumber']
    objects = Manager()
    class Meta:
        unique_together = ('email',)

    phoneNumber = models.CharField(max_length=200)
    isHelper = models.BooleanField(default=True)
    age = models.SmallIntegerField()

    def __str__(self):
        return self.user.name
