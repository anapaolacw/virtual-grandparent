from django.urls import include, path

from . import views

urlpatterns =  [
    path('', views.base, name='base')
]