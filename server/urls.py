
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

class ProductCreateSchema(ModelSchema):
    class Meta:
        model = products
        fields = ['search_image','styleid','brands_filter_facet','price','product_additional_info']
@api.post('/insertproduct', response=list[ProductSchema])

def insert_products(request, payload: ProductCreateSchema):
    new_product = products.objects.create(
        search_image=payload.search_image,
        styleid=payload.styleid,
        brands_filter_facet=payload.brands_filter_facet,
        price=payload.price,
        product_additional_info=payload.product_additional_info
    )

    # Lưu đối tượng sản phẩm vào cơ sở dữ liệu
    new_product.save()
    return new_product

@api.post("/products/bulk")
def create_products(request, product_data: list[dict]):
    product_instances = []
    for data in product_data:
        product = products(
            search_image=data.get("search_image", ""),
            styleid=data.get("styleid", 0),
            brands_filter_facet=data.get("brands_filter_facet", ""),
            price=data.get("price", 0),
            product_additional_info=data.get("product_additional_info", ""),
        )
        product_instances.append(product)

    products.objects.bulk_create(product_instances)
    return {"message": "Products created successfully"}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
