from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
import random
from .models import Product, Category, Comment, favorite
from django.db.models import Q
from .forms import AddToCartForm, CommentForm
from django.contrib import messages
from cart.cart import Cart



# dans url on aura request/category_slug/pro_slug
def product(request, category_slug, product_slug):
    cart = Cart(request)
    all_category = Category.objects.all()
    product = get_object_or_404(
        Product, category__slug=category_slug, slug=product_slug)
    forme = AddToCartForm(request.POST or None)
    form = CommentForm(request.POST or None)
    
    if request.method == 'POST':

        if 'comment' in request.POST:
            if form.is_valid():
                comment = form.save(commit=False)
                comment.client = request.user.client
                comment.product = product
                comment.save()

                return redirect('detail', category_slug=category_slug, product_slug=product_slug)
        elif 'cart' in request.POST:
            if forme.is_valid():
                quantity = forme.cleaned_data['quantity']
                cart.add(product_id=product.id,
                         quantity=quantity, update_quantity=False)
                messages.success(request, 'the product was added to the cart')
                return redirect('detail', category_slug=category_slug, product_slug=product_slug)

        else:
            try:
                favo = favorite.objects.get(
                    client=request.user.client, product=product)
            except favorite.DoesNotExist:
                favo = None
            print('ayoub', favo)
            if favo is None:
                fav=favorite.objects.create(client=request.user.client,product=product)
                fav.save()
                return redirect('detail', category_slug=category_slug, product_slug=product_slug)

    else:
        forme = AddToCartForm()
        form = CommentForm()
      

    similar_products = list(product.category.products.exclude(
        id=product.id))  # all similar products , except our product
    if len(similar_products) >= 4:
        # si les produits similaires de len plus que 4 , on choisit 4 aleatoirement(by la methode sample de random)
        similar_products = random.sample(similar_products, 4)

    comments = Comment.objects.filter(product=product)
    favs = favorite.objects.filter(product=product).count()

    print('comments', comments)
    context = {'forme': forme, 'form': form, 'product': product,
               'similar_products': similar_products, 'all_category': all_category, 'comments': comments, 'favs': favs}
    return render(request, 'product/product.html', context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    all_category = Category.objects.all()
    context = {'category': category, 'all_category': all_category}
    return render(request, 'product/category.html', context)
