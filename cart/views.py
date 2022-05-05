from django.contrib.auth.decorators import login_required
from vendor.models import Client, Vendor
from product.models import Order, Product
from django.http.response import JsonResponse
from cart.cart import Cart
from django.shortcuts import render, redirect
from .cart import Cart
import json

# Create your views here.
# [{},{}]


def data(n):
    L = []
    for i in n:
        L += [i]
    return L
# def index(data):
    # vendors={}
    # products={}
    # for dict in data:
    #     vendors+=dict['product'].vendor
    #     products+=dict['product']

    # return vendors,products


def vendor(data):
    ven = ""
    for dict in data:
        ven += str(dict['product'].vendor)+","
    return ven


def product(data):
    ven = ""
    for dict in data:
        ven += str(dict['product'].title)+","
    return ven


def Quantity(data):
    quantity = ""
    for dict in data:
        quantity += str(dict['quantity'])+","
    return quantity


@login_required
def detail(request):
    client = request.user.client
    cart = Cart(request)
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')

    context = {'cart': Cart(request), 'client': client,
               'vendor': vendor(data(cart)),
               'product': product(data(cart)), 'quantity': Quantity(data(cart))}

    return render(request, 'cart/cart.html', context)


def payementComplete(request):
    body = json.loads(request.body)

    print('BODY:', body)
    v = body['vendor'].split(",")
    p = body['product'].split(",")
    q = body['quantity'].split(",")
    print("vendoooooor", v)
    print("produttt", p)

    vendor = Vendor.objects.filter(username__in=v)
    client = Client.objects.get(username=body['client'])
    product = Product.objects.filter(title__in=p)
    print('VENDER', vendor)
    for vend, pro, quan in zip(vendor, product, q):
        print(vend, pro, client)
        order = Order.objects.create(
            clientusername=client, vendorid=vend, productid=pro, quantity=quan, country=client.country, gender=client.gender, price=pro.price)
        order.save()
        

    return JsonResponse('Payament Completed !', safe=False)
