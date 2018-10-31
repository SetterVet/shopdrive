
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Good, Bill, Order
from django.http import HttpResponseRedirect

import json


# Create your views here.
def profile_item(request, pk):
    request.session['user_id'] = pk
    current_user = User.objects.get(pk=pk)
    bills = Bill.objects.filter(user=current_user)
    for item in bills:
        item.set_total_price()
        item.save()
    return render(request, 'shop/profileuser.html', {'user': current_user, 'bills': bills})


def shophome(request):
    if request.method == 'POST':
        postemail = request.POST['mail']
        try:
            user = User.objects.get(email=postemail)
            print(user)
            return HttpResponseRedirect("/user/" + str(user.pk))
        except User.DoesNotExist:
            content = "This email not in database . Please register"
            return render(request, 'shop/index.html', {'content': content})

    return render(request, 'shop/index.html')


def shopgood(request):
    goods = Good.objects.all()
    return render(request, 'shop/goodlist.html', {'goods': goods})


def room(request):
    if request.method == 'POST':
        postemail = request.POST['mail']
        try:
            user = User.objects.get(email=postemail)
            print(user)
            return HttpResponseRedirect("/user/" + str(user.pk))
        except User.DoesNotExist:
            content = "This email not in database . Please register"

            return render(request, 'shop/room.html', {'content': content})
    return render(request, 'shop/room.html')

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')
