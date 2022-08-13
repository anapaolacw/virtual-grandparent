from django.urls import path

from . import views

app_name = 'core'

urlpatterns =  [
   path('', views.home, name='home'),
   path('menu/', views.oldMenu, name='menu'),
   path('menu/', views.helperMenu, name='menuHelper'),
   path('helpRequests/', views.helpRequests, name='helpRequests'),
   path('createHelpRequest/', views.createHelpRequest, name='createHelpRequest'),
]