from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(products)

class PostMultiple(admin.StackedInline):
    model = products
class PostLastestAdmin(admin.ModelAdmin):
    class Meta:
        model = products
