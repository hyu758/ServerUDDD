
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI, ModelSchema
from api import views
from api.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from .forms import *
from .vnpay import *

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
@api.get("/getProductByEmail/{email}")
def getProductByEmail(request, email: str):
    try:
        product_ids = shopping_cart.objects.filter(email=email).values_list('productID', flat=True)
        # Khởi tạo danh sách để lưu các thông tin sản phẩm
        product_list = []
        quantityOfPr = {}
        for id in product_ids:
            if (id not in quantityOfPr):
                quantityOfPr[id] = 1
            else:
                quantityOfPr[id] += 1
        # Lặp qua từng sản phẩm trong giỏ hàng để lấy thông tin chi tiết của sản phẩm từ bảng Product
        for id in quantityOfPr:
            product = products.objects.get(id=id)

            # Tạo một từ điển đại diện cho thông tin sản phẩm và số lượng trong giỏ hàng
            product_info = {
                "id": product.id,
                "productName": product.productName,
                "price": product.price,
                "image": product.image,
                "brand": product.brand,
                "yearOfManufacture": product.yearOfManufacture,
                "description": product.description,
                "quantity": quantityOfPr[id]  # Số lượng sản phẩm trong giỏ hàng
            }

            # Thêm thông tin sản phẩm vào danh sách sản phẩm
            product_list.append(product_info)
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
    

class orderSchema(ModelSchema):
    class Meta:
        model = order
        fields = ['orderLabel','email', 'fullName', 'address', 'phoneNumber', 'totalAmount', 'token']

@api.post("/insertOrder")
def insertOrder(request, payload : orderSchema):
    try:
        new_order = order.objects.create(
            orderLabel = payload.orderLabel,
            email = payload.email,
            fullName = payload.fullName,
            address = payload.address,
            phoneNumber = payload.phoneNumber,
            totalAmount = payload.totalAmount,
            token = payload.token
        )
        new_order.save()
        return {"message": "Added to order successfully"}
    except Exception as e:
        return {"error": e}


class updateOrderToken(ModelSchema):
    class Meta:
        model = order
        fields = ['token']

@api.put("/updateOrderByID/{orderID}")
def updateOrderByID(request, orderID, payload: updateOrderToken):
    try:
        order_to_update = get_object_or_404(order, id = orderID)
        order_to_update.token = payload.token
        order_to_update.save()
        return {"message": "Order token updated successfully"}
    except Exception as e:
        return {"error": str(e)}


@api.delete("/clearShoppingCartByEmail/{email}")
def clear_shopping_cart(request, email: str):
    try:
        shopping_cart.objects.filter(email = email).delete()
        return {"message": "All items in the shopping cart have been removed successfully"}
    except Exception as e:
        return {"error": str(e)}


class getOrderSchema(ModelSchema):
    class Meta:
        model = order
        fields = '__all__'

@api.get("/getOrderByEmail/{email}", response=list[getOrderSchema])
def getOrderByEmail(request, email : str):
    try:
        orders = order.objects.filter(email = email)
        return list(orders)
    except Exception as e:
        return {"error": str(e)}



@api.get("/paymentSuccess/{orderLabel}")
def getPayment(request, orderLabel : str ):
    result = payment_return(request)
    response = request.GET
    content = {
        'vnp_TransactionNo':response['vnp_TransactionNo']
    }
    if result:
        cur_order = order.objects.get(orderLabel = orderLabel)
        cur_order.token = content['vnp_TransactionNo']
        cur_order.save()
        return "Thanh toan thanh cong"
    return "Thanh toan that bai"


@api.post("/payment/{amountAndOrderLabel}")
def pay(request, amountAndOrderLabel: str):
    try:
        tmp = amountAndOrderLabel.split('_')
        print(tmp)
        order_id = datetime.now().strftime("%Y%m%d%H%M%S")
        print(order_id)
        order_type = "billpayment"
        amount = int(tmp[0])
        order_desc = "aloaloalaoal"
        bank_code = ""
        language = "vn"
        form = PaymentForm({
            'order_id': order_id,
            'order_type': order_type,
            'amount': amount,
            'order_desc': order_desc,
            'bank_code': bank_code,
            'language': language
        })

        result = active_payment(request, form, tmp[1])
        print(result)
        if result:
            return result
    except Exception as e:
        return {"error": str(e)}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
