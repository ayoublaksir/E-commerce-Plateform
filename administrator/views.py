from product.views import product
from product.models import Product, Order
from django.shortcuts import render
from vendor.models import Vendor, Client, Country
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def administrator(request):
    number_of_vendors = Vendor.objects.all().count()
    number_of_clients = Client.objects.all().count()-1
    number_of_orders = Order.objects.all().count()
    number_of_male_clients = Client.objects.filter(
        gender__gender="male").count()
    number_of_female_clients = Client.objects.filter(
        gender__gender="female").count()
    number_of_male_vendors = Vendor.objects.filter(
        gender__gender="male").count()
    number_of_female_vendors = Vendor.objects.filter(
        gender__gender="female").count()

    countries = Country.objects.all()
    client_countries_string = ""
    client_country_data = ""
    vendor_countries_string = ""
    vendor_country_data = ""
    for country in countries:
        client_countries_string += country.name+"%"
        client_country_data += str(country.clients.count())+"%"
        print('clienttt_country_data', client_country_data)

        vendor_countries_string += country.name+"%"
        vendor_country_data += str(country.vendors.count())+"%"

    context = {"vendors": number_of_vendors, "clients": number_of_clients,
               "male_clients": number_of_male_clients,
               "male_vendors": number_of_male_vendors, "female_clients": number_of_female_clients, "female_vendors": number_of_female_vendors,
               "client_countries_string": client_countries_string, "client_country_data": client_country_data, "vendor_countries_string": vendor_countries_string, "vendor_country_data": vendor_country_data,
               "number_of_orders": number_of_orders}

    return render(request, 'administrator/administrator.html', context)


@login_required
def validation(request):

    products = Product.objects.filter(state='pending')
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        if request.POST.get('accept'):
            product.state = "accepted"
            product.save()
        elif request.POST.get('refuse'):
            product.state = "refused"
            product.save()
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

    context = {'products': products, 'paginate': True}
    return render(request, 'administrator/product_validation.html', context)


# "male_clients": number_of_male_clients,
    # "male_vendors": number_of_male_vendors, "female_clients": number_of_female_clients, "female_vendors": number_of_female_vendors}
