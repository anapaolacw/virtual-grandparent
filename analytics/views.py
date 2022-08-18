from django.shortcuts import render
from django.http import HttpResponse

from .models import Transaction

# Create your views here.
def transactions(request):
    return HttpResponse(Transaction.objects.all())
