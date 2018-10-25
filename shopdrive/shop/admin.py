from django.contrib import admin
from .models import Bill,Good,User,Order
# Register your models here.
admin.site.register(Bill)
admin.site.register(Good)
admin.site.register(User)
admin.site.register(Order)