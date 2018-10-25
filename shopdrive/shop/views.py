from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Good, Bill, Order

import json


# Create your views here.
def shophome(request):
    if request.method=='POST':
        postemail=request.POST['mail']
        user=User.objects.get(email=postemail)

        if user.email==postemail:
            print(user)
            return HttpResponse('<h1>Find User</h1>')



    return render(request, 'shop/index.html')



def shopgood(request):
    goods=Good.objects.all()
    return render(request, 'shop/goodlist.html', {'goods': goods})