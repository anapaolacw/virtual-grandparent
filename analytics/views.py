from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Transaction

# Create your views here.
def transactions(request):
    transactions = Transaction.objects.all()
    json = serializers.serialize('json', transactions)
    return HttpResponse(json, content_type='application/json')
