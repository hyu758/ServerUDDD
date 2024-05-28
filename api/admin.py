from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(products)
admin.site.register(accounts)
admin.site.register(shopping_cart)
admin.site.register(order)

