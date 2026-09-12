from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,Category,Cart,CartItem



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

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total = cart.total_price

    context = {
        'cart_items' : cart_items,
        'total' : total,
    }
    return render(request,'cart.html',context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('marketplace:cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()

    return redirect('marketplace:cart')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = cart.total_price

    if request.method == 'POST':
        if request.user.balance >= total:
            request.user.balance -= total
            request.user.save()
            cart.items.all().delete()
            return redirect('accounts:customer_panel')
        else:
            return render(request, 'cart.html', {
                'cart_items': cart.items.all(),
                'total': total,
                'error': 'موجودی کافی نیست',
            })

    return render(request, 'cart.html', {
        'cart_items': cart.items.all(),
        'total': total,
    })