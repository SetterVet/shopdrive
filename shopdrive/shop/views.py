from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Good, Bill, Order
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import json
from datetime import datetime


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
        return render(request, 'shop/index.html', {'login': request.session['user_id']})
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
    if request.method == 'POST' and 'user_id' in request.session:
        current_user = User.objects.get(pk=request.session['user_id'])
        created_bill_pk = Bill.create(user=current_user, godate=request.POST['expected_date'])
        current_bill = Bill.objects.get(pk=created_bill_pk)
        today = datetime.date(datetime.today())
        current_goods = goods.filter(end_date__gte=today)

        for item in current_goods:
            if request.POST[str(item.pk)] != '':
                good_item = Good.objects.get(pk=item.pk)
                item_order = Order.create(bill=current_bill, good=good_item, count=request.POST[str(item.pk)])
                current_bill_order = Order.objects.get(pk=item_order)
                current_bill_order.delete_unit_from_shop()
                if current_bill_order.delete_from_shop == False:
                    current_bill_order.delete()

        current_bill.set_total_price()
        current_bill.save()
        return HttpResponseRedirect('/user/' + str(request.session['user_id']))
    elif 'user_id' in request.session:
        today = datetime.date(datetime.today())
        print(today)
        return render(request, 'shop/goodlist.html', {'goods': goods, 'login': True, 'today': today})
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
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['mail']).all():
            return render(request, 'shop/index.html',
                          {'content': "Користувач з таким email вже зареєстрований увійдіть в свій кабінет"})
        else:
            User.create(first=request.POST['first'], last=request.POST['last'], email=request.POST['mail'])
            current_user = User.objects.get(email=request.POST['mail'])
            return HttpResponseRedirect("/user/" + str(current_user.pk))

    return render(request, 'shop/registration.html')



def deletebill(request,pk):
    current_bill=Bill.objects.get(pk=pk)
    current_bill.delete_bill()
    return HttpResponseRedirect('/user/'+str(request.session['user_id']))

def editbill(request,pk):
    if request.method == 'POST' and 'user_id' in request.session:
        goods=Good.objects.all()

        check_current_bill=Bill.objects.get(pk=pk).check_id
        current_bill = Bill.objects.get(check_id=check_current_bill)
        today = datetime.date(datetime.today())
        current_goods = goods.filter(end_date__gte=today)
        orders=Order.objects.filter(id_bill=current_bill).all()
        for item in orders:
            item.delete_order()



        for item in current_goods:
            if request.POST[str(item.pk)] != '':
                good_item = Good.objects.get(pk=item.pk)
                item_order = Order.create(bill=current_bill, good=good_item, count=request.POST[str(item.pk)])
                current_bill_order = Order.objects.get(pk=item_order)
                current_bill_order.delete_unit_from_shop()
                if current_bill_order.delete_from_shop == False:
                    current_bill_order.delete()

        current_bill.set_total_price()
        current_bill.save()
        return HttpResponseRedirect('/user/' + str(request.session['user_id']))
    else:
        current_bill=Bill.objects.get(pk=pk)
        orders=Order.objects.filter(id_bill=current_bill).all()
        today=datetime.date(datetime.now())
        goods=Good.objects.filter(end_date__gte=today).all()
        goods_in_bill = list()
        for item in orders:
            goods_in_bill.append(item.id_good)
        goods_not_in_bill=list()
        for item in goods:
            if item not in goods_in_bill:
                goods_not_in_bill.append(item)
        current_user=User.objects.get(pk=request.session['user_id'])
        today=datetime.date(datetime.today())
        return render(request, 'shop/editbill.html', {'bill': current_bill, 'orders': orders,
                      'in_bill':goods_in_bill,'not_in_bill':goods_not_in_bill,'user':current_user,'today':today})

