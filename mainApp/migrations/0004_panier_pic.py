# Generated by Django 3.1.4 on 2021-01-03 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_remove_panier_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='panier',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
    ]
