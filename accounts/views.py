from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('accounts:profile')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def customer_panel_view(request):
    return render(request, 'customer_panel.html', {'customer': request.user})


@login_required
def payment_view(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
        except (TypeError, ValueError):
            amount = 0
        if 0 < amount <= 50_000_000: 
            request.user.balance += amount
            request.user.save(update_fields=['balance'])
            return redirect('accounts:customer_panel')
    return render(request, 'payment.html')


@login_required
def order_history_view(request):
    return render(request, 'order_history.html', {'orders': []})