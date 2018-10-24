from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Good,Bill,Good_item_in_bill
import json
# Create your views here.
def shophome(request):
    emails =[]
    user_list = User.objects.all()
    for user in user_list:
        emails.append(user.email)
    print(emails)

    return HttpResponse("<h1>Main Page</h1>")