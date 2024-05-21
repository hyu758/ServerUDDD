
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, ModelSchema
from api.models import *

api = NinjaAPI()

class ProductSchema(ModelSchema):
    class Meta:
        model = products
        fields = '__all__'
@api.get('/product', response=list[ProductSchema], by_alias=True)
def get_products(request):
    return products.objects.all()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
