from django.db import models

# Create your models here.
class products(models.Model):
    image = models.TextField(default='')
    productName = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    brand = models.CharField(max_length=50)
    yearOfManufacture = models.IntegerField(default=0)
    description = models.TextField(default='')

class accounts(models.Model):
    firstName = models.CharField(max_length=20, default="")
    lastName = models.CharField(max_length=20, default="")
    email = models.EmailField(unique=True, default="")
    password = models.CharField(max_length=20)

class shopping_cart(models.Model):
    productID = models.IntegerField(default=0)
    email = models.EmailField()  # Sử dụng email thay vì account_id
    token = models.TextField(default="")

class order(models.Model):
    orderLabel = models.TextField(default="")
    email = models.EmailField()
    fullName = models.CharField(max_length=30, default="")
    address = models.TextField(default="")
    phoneNumber = models.CharField(max_length=20, default="")
    totalAmount = models.BigIntegerField(default=0)
    token = models.TextField(default="")
    firstOrderImage = models.TextField(default="")