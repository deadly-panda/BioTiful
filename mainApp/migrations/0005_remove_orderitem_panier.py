# Generated by Django 3.1.4 on 2021-01-03 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_panier_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='panier',
        ),
    ]