# Generated by Django 2.1.2 on 2018-11-01 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order_delete_from_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='a@com', max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='first_name', max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='last_name', max_length=60),
        ),
    ]
