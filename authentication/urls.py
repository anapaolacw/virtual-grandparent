from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'
urlpatterns =  [
    path('signup/<str:typeOfUser>', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]

    