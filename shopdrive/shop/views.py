from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Good, Bill, Order
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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
    if 'user_id' in request.session:
        return render(request, 'shop/index.html', {'login':request.session['user_id']})
    elif request.method == 'POST':
        postemail = request.POST['mail']
        try:
            user = User.objects.get(email=postemail)
            print(user)
            return HttpResponseRedirect("/user/" + str(user.pk))
        except User.DoesNotExist:
            content = "This email not in database . Please register"
            return render(request, 'shop/index.html', {'content': content})

    else:
        return render(request, 'shop/index.html')


def shopgood(request):
    goods = Good.objects.all()
    if 'user_id' in request.session:
        return render(request, 'shop/goodlist.html', {'goods': goods, 'login': True})
    else:
        return render(request, 'shop/goodlist.html', {'goods': goods, 'login': False})


def room(request):
    if 'user_id' in request.session:
        try:
            user = User.objects.get(pk=request.session['user_id'])
            print(user)
            return HttpResponseRedirect("/user/" + str(user.pk))
        except User.DoesNotExist:
            content = "This email not in database . Please register"

            return render(request, 'shop/room.html', {'content': content})

    elif request.method == 'POST':
        postemail = request.POST['mail']
        try:
            user = User.objects.get(email=postemail)
            print(user)
            return HttpResponseRedirect("/user/" + str(user.pk))
        except User.DoesNotExist:
            content = "This email not in database . Please register"

            return render(request, 'shop/room.html', {'content': content})

    else:
        return render(request, 'shop/room.html')


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def registration(request):
    if request.method=='POST':
        if User.objects.filter(email=request.POST['mail']).all():
            return render(request, 'shop/index.html',{'content':"Користувач з таким email вже зареєстрований увійдіть в свій кабінет"})
        else:
            User.create(first=request.POST['first'],last=request.POST['last'],email=request.POST['mail'])
            current_user=User.objects.get(email=request.POST['mail'])
            return HttpResponseRedirect("/user/"+str(current_user.pk))

    return render(request, 'shop/registration.html')