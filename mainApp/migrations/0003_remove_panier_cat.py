# Generated by Django 3.1.4 on 2021-01-03 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_auto_20210103_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panier',
            name='cat',
        ),
    ]