from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Good, Bill, Order

import json


# Create your views here.
def shophome(request):
    return render(request, 'shop/index.html')

def auth(request):
    return HttpResponse('<h1>Success</h1>')

def shopgood(request):
    goods=Good.objects.all()
    return render(request, 'shop/goodlist.html', {'goods': goods})