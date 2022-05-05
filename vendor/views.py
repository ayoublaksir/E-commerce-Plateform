from django.db.models import Count
from django.core.checks import messages
from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Vendor, Country, Gender
from django.contrib.auth.decorators import login_required
from product.models import Category, Product, Order
from .forms import ClientInscriptionForm, ProductForm
from django.utils.text import slugify
from django.db import transaction
from django.views.generic import CreateView
from .forms import VendorInscriptionForm, ClientInscriptionForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Une transaction regroupe plusieurs requêtes à effectuer. Si l'une d'elles échoue, toutes les précédentes sont annulées et les items retournent à leur état original
# Create your views here.


# def become_vendor(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             vendor = Vendor.objects.create(
#                 name=user.username, created_by=user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     context = {'form': form}

#     return render(request, 'vendor/become_vendor.html', context)

def earning(orders):
    total = 0
    for order in orders:
        total += order.price*order.quantity
    return total


def client_country(country, request):
    orders = country.orders.filter(vendorid=request.user.vendor)
    query = orders.query
    query.group_by = ['clientusername']
    resu = QuerySet(query=query, model=Country)
    results = QuerySet(query=query, model=Country).count()
    return results, resu


def client_gender(request):
    L = []
    for gender in Gender.objects.all():
        L += [gender.orders.filter(vendorid=request.user.vendor).values(
            'clientusername').annotate(dcount=Count('clientusername')).order_by().count()]
    return L


def client_cou(request):
    L = {}
    for country in Country.objects.all():
        L[str(country)] = country.orders.filter(vendorid=request.user.vendor).values(
            'clientusername').annotate(dcount=Count('clientusername')).order_by().count()
    return L


# def history_earning(request):
#    vendor=request.user.vendor
#    orders= vendor.orders.group_by('date_added')
#    for order in orders:
#        print("hiiiiiiii",order.date_added)


@transaction.atomic
@login_required
def vendor_admin(request):
    orders = Order.objects.filter(vendorid=request.user.vendor)
    # for males and females
    males = client_gender(request)[0]
    females = client_gender(request)[1]

    # print('females',females)
    # endfor

    total_earning = earning(orders)

    countries = Country.objects.all()

    # top buyers:
    buyers = Vendor.objects.annotate(
        count=Count('orders')).order_by('-count')[0:5]
    buyer_country = ""
    buyer_orders = ""
    for buyer in buyers:
        buyer_country += str(buyer.country)+"%"
        buyer_orders += str(buyer.orders.count())+"%"
    print("buyer_country:", buyer_country)
    print("buyer_orders:", buyer_orders)

    print('buyers', buyers)
    # earning history

    # endearning

    # end buyers

    client_countries_string = ""
    client_country_data = ""
    for country in countries:
        client_countries_string += country.name+"%"
        client_country_data += str(client_cou(request)[str(country)])+"%"
    print('client_country_data', client_country_data, client_countries_string
          )

    total_orders = orders.count()

    client_number = males+females
    print('orders', orders)
    # user reference to (user qu'on a creer by login request, user) and vendor reference to related_name in models
    vendor = request.user.vendor
    products = vendor.product.all()
    context = {'vendor': vendor, 'products': products, 'client_number': client_number, 'total_orders': total_orders,
               'total_earning': total_earning, 'client_countries_string': client_countries_string, 'client_country_data': client_country_data, 'males': males, 'females': females,
               'buyer_country': buyer_country, 'buyer_orders': buyer_orders}
    return render(request, 'vendor/vendor_admin.html', context)


@login_required
def add_product(request):
    vendor = request.user.vendor
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.slug = slugify(product.title)
            product.country = vendor.country
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    context = {'form': form, "vendor": vendor}

    return render(request, 'vendor/add_product.html', context)


@login_required
def product_delete(request, pk):
    vendor = request.user.vendor
    item = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('products')
    context = {'item': item, 'vendor': vendor}
    return render(request, 'vendor/delete.html', context)


class vendor_register(CreateView):
    model = User
    form_class = VendorInscriptionForm
    template_name = 'vendor/become_vendor.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('vendor_admin')


class client_register(CreateView):
    model = User
    form_class = ClientInscriptionForm
    template_name = 'client/become_client.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if username == "ayoub_admin" and password == "ayoub_adminayoub_admin":
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('administrator')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_vendor:
                    login(request, user)
                    return redirect('vendor_admin')
                else:
                    login(request, user)
                    return redirect('home')
            else:
                messages.Error(request, "Invalid username or password")
        else:
            messages.Error(request, "Invalid username or password")
    context = {'form': AuthenticationForm()}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def products_state(request):
    vendor = request.user.vendor
    products = vendor.product.all()
    paginator = Paginator(products, 6)  # six items in page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # if page not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver the last page
        products = paginator.page(paginator.num_pages)

    context = {'vendor': vendor, 'products': products,  'paginate': True}
    return render(request, 'vendor/products_state.html', context)


@login_required
def products(request):

    vendor = request.user.vendor
    products = vendor.product.all()
    paginator = Paginator(products, 6)  # six items in page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # if page not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver the last page
        products = paginator.page(paginator.num_pages)

    context = {'vendor': vendor, 'products': products,  'paginate': True}
    return render(request, 'vendor/products.html', context)


def Clients(request):
    vendor = request.user.vendor
    orders = vendor.orders.all()
    for order in orders:
        print(order.productid)
    print('orders', orders)
    context = {'vendor': vendor, 'orders': orders}
    return render(request, 'vendor/Clients.html', context)
