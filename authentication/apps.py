from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'
    INVALID_CREDENTIALS_MESSAGE = "Invalid Credentials Provided."
