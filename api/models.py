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