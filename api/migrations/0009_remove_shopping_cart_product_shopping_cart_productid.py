# Generated by Django 5.0.6 on 2024-05-27 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_shopping_cart_delete_shoppingcart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopping_cart',
            name='product',
        ),
        migrations.AddField(
            model_name='shopping_cart',
            name='productID',
            field=models.IntegerField(default=0),
        ),
    ]