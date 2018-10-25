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
    total_price = models.DecimalField(decimal_places=2, max_digits=10000000, default=0.00)
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
        self.total_price = total_price
        self.save()


class Order(models.Model):
    id_bill = models.ForeignKey(Bill, related_name='bill', on_delete=models.CASCADE)
    id_good = models.ForeignKey(Good, related_name='good', on_delete=models.CASCADE)
    count = models.DecimalField(decimal_places=2, max_digits=100000)
    delete_from_shop = models.BooleanField(default=False)

    def __str__(self):
        return "Add to " + str(self.id_bill.__str__) + " bill " + str(self.id_good.__str__)

    def delete_unit_from_shop(self):
        if self.delete_from_shop == False:
            good_item = Good.objects.get(id=self.id_good.id)
            if good_item.count > self.count:
                good_item.count -= float(self.count)
                self.delete_from_shop=True
                self.save()
                good_item.save()



            else:
                print("Can not deleten enough good")

        else:
            print("Already Deleted")
