from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from product.views import product
from vendor.models import Country
from django.core import paginator
from django.shortcuts import render
from product.models import Product, Category, Order, favorite
from django.db.models import Q, query
# paginator pour avoir diviser le contenu en pls pages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
from product.filter import ProductFilter
import datetime

from django import template
register = template.Library()

# Method 1 for django queryset (Better)


def listes(category):
    L = []
    for categ in category:
        categ = [categ.products.filter(state='accepted')]
        L += [categ]
    return L


def home(request):
    products = Product.objects.filter(state='accepted')

    news_products = random.sample(list(products),len(list(products)))
    all_category = Category.objects.all()

    context = {'news_products': news_products,
               'all_category': all_category, 'paginate': True, 'liste': listes(all_category)}

    return render(request, 'interieur/home.html', context)


@login_required
def favorites(request):
    favorites = favorite.objects.filter(
        client=request.user.client)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        favorit = favorite.objects.get(
            client=request.user.client, product=product_id)
        favorit.delete()

    all_category = Category.objects.all()
    context = {'favorites': favorites, 'all_category': all_category}
    return render(request, 'interieur/favorite.html', context)


def search(request):
    query = request.GET['query']
    category_name = request.GET['category_name']

    countries = Country.objects.all()
    all_category = Category.objects.all()
    products_list = Product.objects.filter(
        (Q(title__icontains=query) | (Q(description__icontains=query))), category__title__icontains=category_name, state='accepted')
    if request.method == 'POST':
        max = request.POST.get('max')
        country = request.POST.get('country')

        if country == 'All' and max == '':  # important
            pass
        if country == 'All' and max != '':
            products_list = products_list.filter(price__lte=max)
        if country != 'All' and max == '':
            products_list = products_list.filter(
                vendor__country__name=country)
        if country != 'All' and max != '':
            products_list = products_list.filter(
                Q(vendor__country__name=country), Q(price__lte=max))

    all_category = Category.objects.all()

    paginator = Paginator(products_list, 20)  # six items in page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # if page not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver the last page
        products = paginator.page(paginator.num_pages)
    context = {'query': query, 'products': products, 'countries': countries,
               'paginate': True, 'all_category': all_category, "category_name": category_name}
    return render(request, 'product/search.html', context)


def all_products(request):

    now = datetime.datetime.now()

    countries = Country.objects.all()
    all_products = Product.objects.filter(state='accepted')
    all_category = Category.objects.all()
    if request.method == 'POST':
        max = request.POST.get('max')
        country = request.POST.get('country')

        if country == 'All' and max == '':  # important
            pass
        if country == 'All' and max != '':
            all_products = Product.objects.filter(price__lte=max)
        if country != 'All' and max == '':
            all_products = Product.objects.filter(
                vendor__country__name=country)
        if country != 'All' and max != '':
            all_products = Product.objects.filter(
                Q(vendor__country__name=country), Q(price__lte=max))

    paginator = Paginator(all_products, 20)  # six items in page
    page = request.GET.get('page')
    try:
        all_products = paginator.page(page)
    except PageNotAnInteger:
        # if page not an integer deliver the first page
        all_products = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver the last page
        all_products = paginator.page(paginator.num_pages)

    context = {
        'all_products': all_products,
        'paginate': True,
        'all_category': all_category,

        'countries': countries,
        'now': now

    }

    return render(request, 'interieur/all_products.html', context)


@login_required
def order(request):
    client = request.user.client
    all_orders = client.orders.all()
    all_category = Category.objects.all()
    context = {'all_orders': all_orders,
               'client': client, 'all_category': all_category}
    return render(request, 'client/orders.html', context)
