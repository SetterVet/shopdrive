from django.db import models

# Create your models here.
class Good(models.Model):
    name = models.CharField(max_length=256, blank=False, verbose_name="Name")
    weight_and_unit = models.CharField(max_length=64, blank=False, verbose_name='weight_and_unit')
    count = models.IntegerField(verbose_name="count")
    price = models.DecimalField(verbose_name="price", decimal_places=2 ,max_digits=100000)
    end_date = models.DateField()



class Order(models.Model):
    id_goods = models.ManyToManyField(Good)
    check_id = models.IntegerField(verbose_name='check_id', default=0, unique=True)
    expected_date = models.DateField()



class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()