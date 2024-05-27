
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI, ModelSchema
from api import views
from api.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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
        fields = ['productID', 'email', 'quantity', 'token']

@api.post("/add_to_shopping_cart")
def add_to_shopping_cart(request, payload: ShoppingCartSchema):
    try:
        # Tạo một đối tượng shopping_cart mới từ dữ liệu được cung cấp
        new_cart_item = shopping_cart.objects.create(
            productID=payload.productID,
            email=payload.email,
            quantity = payload.quantity,
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
@api.get("/getProductByID/{productID}", response=getProductByID)
def getProductByID(request, productID : int):
    try:
        product = products.objects.get(pk = productID)
        return product
    except products.DoesNotExist:
        return {"error": "Product not found"}


class getProductByEmail(ModelSchema):
    class Meta:
        model = products
        fields = '__all__'
@api.get("/getProductByEmail/{email}")
def getProductByEmail(request, email: str):
    try:
        # Lấy tất cả ID
        product_ids = shopping_cart.objects.filter(email=email).values_list('productID', flat=True)
        # Lấy tất cả các sản phẩm tương ứng từ bảng products
        product_list = []
        for id in product_ids:
            print(id)
            product = products.objects.get(id=id)
            product_info = {
                "id": product.id,
                "productName": product.productName,
                "price": product.price,
                "image": product.image,
                "brand": product.brand,
                "yearOfManufacture": product.yearOfManufacture,
                "description": product.description,
                "quantity": (shopping_cart.objects.get(productID = id)).quantity  # Số lượng sản phẩm trong giỏ hàng
            }
            product_list.append(product_info)

        # Trả về danh sách sản phẩm dưới dạng JSON
        return JsonResponse(product_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api.delete("/removeProductByID/{product_id}")
def remove_product(request, product_id: int):
    try:
        # Tìm sản phẩm cần xoá từ cơ sở dữ liệu
        cart_item = shopping_cart.objects.filter(productID=product_id).first()

        # Xoá mục trong giỏ hàng
        if cart_item:
            # Nếu tìm thấy mục trong giỏ hàng, thì xoá nó
            cart_item.delete()
            return {"message": "Cart item removed successfully"}
        else:
            # Nếu không tìm thấy mục trong giỏ hàng, trả về thông báo lỗi
            return {"error": "Cart item not found with productID {}".format(product_id)}
    except Exception as e:
        return {"error": str(e)}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
