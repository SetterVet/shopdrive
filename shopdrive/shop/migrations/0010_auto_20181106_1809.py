# Generated by Django 2.1.2 on 2018-11-06 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20181105_1435'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='count',
            new_name='count_of_good',
        ),
    ]
