from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'analytics'
urlpatterns =  [
    path('transactions/', views.transactions, name='transactions'),
]

    