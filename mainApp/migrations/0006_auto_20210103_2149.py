# Generated by Django 3.1.4 on 2021-01-03 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_remove_orderitem_panier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainApp.item'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Panier',
        ),
    ]
