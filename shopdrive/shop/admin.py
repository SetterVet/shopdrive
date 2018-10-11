from django.contrib import admin
from .models import Order,Good,User
# Register your models here.
admin.site.register(Order)
admin.site.register(Good)
admin.site.register(User)