from django.db import models

# Create your models here.
class products(models.Model):
    search_image = models.TextField(default='')
    styleid = models.CharField(max_length=30)
    brand_filter_facet = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    product_addtional_info = models.CharField(max_length=100)