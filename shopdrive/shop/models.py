from django.db import models
from random import randrange
import datetime


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=40, default='first_name')
    last_name = models.CharField(max_length=60, default='last_name')
    email = models.EmailField(default='a@com')

    def __str__(self):
        return str(self.last_name) + " " + str(self.first_name)

    @staticmethod
    def create(first, last, email):
        a = User(first_name=first, last_name=last, email=email)
        a.save()


class Good(models.Model):
    name = models.CharField(max_length=256, blank=False, verbose_name="Name")
    weight_and_unit = models.CharField(max_length=64, blank=False, verbose_name='weight_and_unit')
    count = models.DecimalField(verbose_name="count", decimal_places=3, max_digits=10)
    price = models.DecimalField(verbose_name="price", decimal_places=2, max_digits=10)
    end_date = models.DateField()

    def __str__(self):
        return str(self.name) + " " + str(self.weight_and_unit)


class Bill(models.Model):
    check_id = models.IntegerField(verbose_name='check_id', default=0, unique=True)
    expected_date = models.DateField(blank=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True, blank=False)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True, blank=False)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.check_id)

    def set_total_price(self):
        bill_item = Order.objects.filter(id_bill=self)
        good_priceitem, count_item = [], []
        for item in bill_item:
            good_item = Good.objects.get(id=item.id_good.id)
            good_priceitem.append(good_item.price)
            count_item.append(item.count)
        total_price = 0.0
        print(good_priceitem)
        print(count_item)
        for i in range(len(bill_item)):
            total_price += float(good_priceitem[i]) * float(count_item[i])
        self.total_price = round(total_price, 2)
        self.save()

    @staticmethod
    def create(user, godate):
        while True:
            check = randrange(0, 100000)
            if not Bill.objects.filter(check_id=check).all():
                break
        a = Bill(check_id=check, user=user, expected_date=godate)
        a.save()
        return a.pk

    def delete_bill(self):
        orders = Order.objects.filter(id_bill=self).all()
        for item in orders:
            item.delete_order()
        self.delete()


class Order(models.Model):
    id_bill = models.ForeignKey(Bill, related_name='bill', on_delete=models.CASCADE)
    id_good = models.ForeignKey(Good, related_name='good', on_delete=models.CASCADE)
    count = models.DecimalField(decimal_places=3, max_digits=10)
    delete_from_shop = models.BooleanField(default=False)

    def __str__(self):
        return "Add to " + str(self.id_bill.__str__) + " bill " + str(self.id_good.__str__) + "count -" + str(
            self.count)

    def delete_unit_from_shop(self):
        if self.delete_from_shop == False:
            good_item = Good.objects.get(pk=self.id_good.pk)
            if good_item.count > self.count:
                good_item.count -= self.count
                self.delete_from_shop = True
                self.save()
                good_item.save()
                return True


            else:
                print("Can not deleten enough good")
                return False
        else:
            print("Already Deleted")
            return False

    def delete_order(self):
        good_item = Good.objects.get(pk=self.id_good.pk)
        good_item.count += self.count
        self.delete()
        good_item.save()

    @staticmethod
    def create(bill, good, count):
        a = Order(id_bill=bill, id_good=good, count=count)
        a.save()
        return a.pk
