
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI, ModelSchema
from api import views
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
        fields = ['image','productName','price','brand','yearOfManufacture', 'description']


@api.post("/products/bulk")
def create_products(request, product_data: list[dict]):
    product_instances = []
    for data in product_data:
        product = products(
            image=data.get("image", ""),
            productName=data.get("productName", ""),
            price=data.get("price", 0),
            brand=data.get("model", ""),
            yearOfManufacture=data.get("yearOfManufacture", 0),
            description = data.get("specifications", "")
        )
        product_instances.append(product)

    products.objects.bulk_create(product_instances)
    return {"message": "Products created successfully"}


class AccountSchema(ModelSchema):
    class Meta:
        model = accounts
        fields = ['firstName', 'lastName','email', 'password']

@api.post("/insertaccount", response=AccountSchema)
def insertAccountSchema(request, payload : AccountSchema):
    new_account = accounts.objects.create(
        firstName = payload.firstName,
        lastName = payload.lastName,
        email=payload.email,
        password=payload.password,
    )
    new_account.save()
    return new_account


class getAccountSchema(ModelSchema):
    class Meta:
        model = accounts
        fields = '__all__'

@api.get("/getAccount", response=list[getAccountSchema])
def getAccount(request):
    return accounts.objects.all()


class getAccountByEmailSchema(ModelSchema):
    class Meta:
        model = accounts
        fields = ['firstName', 'lastName','email']

@api.get("/getAccountByEmail/{email}", response=getAccountByEmailSchema)
def get_account_by_email(request, email: str):
    try:
        account = accounts.objects.get(email=email)
        return account
    except accounts.DoesNotExist:
        return {"error": "Account not found"}
    

class ShoppingCartSchema(ModelSchema):
    class Meta:
        model = shopping_cart
        fields = ['productID', 'email', 'token']

@api.post("/add_to_shopping_cart")
def add_to_shopping_cart(request, payload: ShoppingCartSchema):
    try:
        # Tạo một đối tượng shopping_cart mới từ dữ liệu được cung cấp
        new_cart_item = shopping_cart.objects.create(
            productID=payload.productID,
            email=payload.email,
            token=payload.token,
        )
        # Lưu đối tượng vào cơ sở dữ liệu
        new_cart_item.save()
        # Trả về thông báo thành công
        return {"message": "Added to shopping cart successfully"}
    except Exception as e:
        # Trả về một thông báo lỗi nếu có lỗi xảy ra
        return {"error": str(e)}
    
class getProductByID(ModelSchema):
    class Meta:
        model = products
        fields = '__all__'
@api.get("/getProductByEmail/{productID}", response=getProductByID)
def getProductByID(request, productID : int):
    try:
        product = products.objects.get(pk = productID)
        return product
    except products.DoesNotExist:
        return {"error": "Product not found"}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
