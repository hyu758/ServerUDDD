from django.db import models

# Create your models here.
class products(models.Model):
    search_image = models.TextField(default='')
    styleid = models.IntegerField(default=0)
    brands_filter_facet = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    product_additional_info = models.CharField(max_length=100)

class accounts(models.Model):
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=20)