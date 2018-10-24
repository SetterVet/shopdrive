from django.db import models


# Create your models here.
class Good(models.Model):
    name = models.CharField(max_length=256, blank=False, verbose_name="Name")
    weight_and_unit = models.CharField(max_length=64, blank=False, verbose_name='weight_and_unit')
    count = models.IntegerField(verbose_name="count")
    price = models.DecimalField(verbose_name="price", decimal_places=2, max_digits=100000)
    end_date = models.DateField()

    def __str__(self):
        return str(self.name) + " " + str(self.weight_and_unit)


class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()

    def __str__(self):
        return str(self.last_name) + " " + str(self.first_name)


class Bill(models.Model):
    check_id = models.IntegerField(verbose_name='check_id', default=0, unique=True)
    expected_date = models.DateField()
    total_price = models.DecimalField(decimal_places=2,max_digits=10000000,default=0.00)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True, blank=False)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True, blank=False)
    user = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.check_id)

    def set_total_price(self):
        bill_item=Good_item_in_bill.objects.filter(bill = self)
        good_item,count_item=[],[]
        for item in bill_item:
            good_item.append(item.good)
            count_item.append(item.count)
        total_price=0.0
        for i in range(len(bill_item)):
            total_price+=good_item[i]*count_item[i]
        self.total_price=total_price


class Good_item_in_bill(models.Model):
    bill=models.ForeignKey(Bill, related_name='bill',on_delete=models.CASCADE)
    good=models.ForeignKey(Good, related_name='good',on_delete=models.CASCADE)
    count= models.DecimalField(decimal_places=2, max_digits=100000)

    def __str__(self):
        return "Add to "+str(self.bill.__str__)+" bill "+str(self.good.__str__)

    def delete_unit_from_shop(self):
        good_item=Good.objects.get(good = self.good)
        if good_item.count>self.count:
            good_item-=self.count
            good_item.save()
            return True
        else:
            return False