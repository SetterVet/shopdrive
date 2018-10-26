from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Good, Bill, Order

import json


# Create your views here.
def profile_item(request,userid):
    current_user=User.objects.get(pk=userid)
    return render(request, 'shop/profileuser.html',{'user':current_user})

def shophome(request):
    if request.method=='POST':
        postemail=request.POST['mail']
        try:
            user=User.objects.get(email=postemail)
            print(user)
            return profile_item(request,user.pk)
        except User.DoesNotExist:
            content="This email not in database . Please register"
            return render(request,'shop/index.html',{'content':content})

    return render(request, 'shop/index.html')



def shopgood(request):
    goods=Good.objects.all()
    return render(request, 'shop/goodlist.html', {'goods': goods})

def room(request):
    if request.method=='POST':
        postemail=request.POST['mail']
        try:
            user=User.objects.get(email=postemail)
            print(user)
            return profile_item(request,user.pk)
        except User.DoesNotExist:
            content="This email not in database . Please register"
            return render(request,'shop/room.html',{'content':content})
    return render(request, 'shop/room.html')