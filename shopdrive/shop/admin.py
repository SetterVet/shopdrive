from django.contrib import admin
from .models import Bill,Good,User,Good_item_in_bill
# Register your models here.
admin.site.register(Bill)
admin.site.register(Good)
admin.site.register(User)
admin.site.register(Good_item_in_bill)