from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import AddBalanceForm
from django.db import transaction



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
def add_balance(request):
    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            user.balance += amount
            user.save(update_fields=['balance'])
            return redirect('marketplace:add_balance')
    else:
        form = AddBalanceForm()
    
    return render(request, 'add_balance.html', {'form': form})

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        messages.error(request, "سبد خرید شما پیدا نشد!")
        return redirect('marketplace:product_list')

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "سبد خرید شما خالی است!")
        return redirect('marketplace:product_list')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.user.balance < total_price:
        messages.error(request, "موجودی کافی نیست! لطفا حساب خود را شارژ کنید.")
        return redirect('marketplace:add_balance')


    with transaction.atomic():
    
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )

        request.user.balance -= total_price
        request.user.save()
        cart_items.delete()

    messages.success(request, "خرید با موفقیت انجام شد!")
    return redirect('marketplace:product_list')



@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})