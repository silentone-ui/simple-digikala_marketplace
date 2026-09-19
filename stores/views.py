from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.http import HttpResponseForbidden
from .models import Store
from .forms import StoreForm,ProductForm
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
        form = StoreForm()

    return render(request, 'create_store.html', {'form': form})


@login_required
def add_product_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user:
        return HttpResponseForbidden("شما اجازه ندارید.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store 
            product.save()
            return redirect('stores:store_detail', store_id=store.id)
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'store': store, 'form': form})


@login_required
def delete_store(request,store_id):
    if request.method=='POST':
        store = Store.objects.get(id=store_id)
        store.delete()
        return redirect('stores:create_store')

    return render(request,'seller_panel.html')
