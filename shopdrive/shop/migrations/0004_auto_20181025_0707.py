# Generated by Django 2.1.2 on 2018-10-25 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20181024_1840'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Good_item_in_bill',
            new_name='Order',
        ),
    ]
