from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import HttpResponseForbidden
from .models import Store
from .forms import StoreForm
from marketplace.models import Category, Product 

def store_list_view(request):
    stores = Store.objects.all()
    return render(request, 'stores.html', {'stores': stores})


def store_detail_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = store.products.all() 

    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'store_detail.html', context)


@login_required
def seller_panel_view(request):
    store = getattr(request.user, 'store', None)
    return render(request, 'seller_panel.html', {'store': store})


@login_required 
def create_store_view(request):
    if hasattr(request.user, 'store'):
        return redirect('stores:seller_panel')

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            
            request.user.is_seller = True
            request.user.save()
            
            return redirect('stores:seller_panel')
        else:
            print(form.errors)
    else:
        form = StoreForm()

    return render(request, 'create_store.html', {'form': form})


@login_required
def add_product_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user:
        return HttpResponseForbidden("شما اجازه اضافه کردن محصول به این فروشگاه را ندارید.")

    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        if name and price and category_id:
            category = get_object_or_404(Category, id=category_id)
            final_slug = slug if slug else slugify(name)

            Product.objects.create(
                name=name,
                slug=final_slug,
                description=description,
                price=price,
                stock=stock,
                category=category,
                store=store,
                image=image,
            )
            return redirect('stores:store_detail', store_id=store.id)
        else:

            pass

    return render(request, 'add_product.html', {
        'store': store,
        'categories': categories,
    })
