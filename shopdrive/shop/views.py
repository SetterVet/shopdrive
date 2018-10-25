from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Good,Bill,Order
import json
# Create your views here.
def shophome(request):
    bill=Bill.objects.all()[0]
    bill_items=Order.objects.filter(id=2)
    print(bill)
    print(bill_items)
    # bill.set_total_price()
    # print(bill.total_price)
    # bill.save()
    goods=Good.objects.all()
    return render(request,'shop/index.html',{'goods':goods})