from django.shortcuts import render,get_object_or_404
from .models import Product,Category


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    contex = {
        'products' :products,
        'categories' : categories,
    }

    return render(request,'home.html',contex)


def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'store_detail.html', context)