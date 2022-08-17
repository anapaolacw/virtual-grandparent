from django.urls import path

from . import views

app_name = 'core'

urlpatterns =  [
   path('', views.home, name='home'),
   path('menu/', views.oldMenu, name='menu'),
   path('helper/menu/', views.helperMenu, name='helperMenu'),
   path('help-requests/', views.helpRequests, name='helpRequests'),
   path('help-requests/all/', views.allHelpRequests, name='allHelpRequests'),
   path('help-request/create/', views.createHelpRequest, name='createHelpRequest'),
   path('help-request/edit/<int:id>', views.editHelpRequest, name='editHelpRequest'),
   path('help-request/delete/<int:id>', views.deleteHelpRequest, name='deleteHelpRequest'),
   path('help-offer/create/<int:id>', views.createHelpOffer, name='createHelpOffer'),
   path('my-offer-help/<int:id>', views.seeOffer, name='seeOffer'),
   path('my-offers', views.myOffers, name='myOffers'),
   path('my-offer/delete/<int:id>', views.deleteHelpOffer, name='deleteHelpOffer'),
   path('my-offer/edit/<int:id>', views.editHelpOffer, name='editHelpOffer'),
]