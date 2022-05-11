from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import Item, Categories
from django.contrib.auth.models import User
from . models import Watchlist, CartItem


def index(request):
    items = Item.objects.all()
    return render(request, 'auth_users/index.html', {'items': items})


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    return render(request, 'auth_users/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'auth_users/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def categories(request):
    items = Categories.objects.all()
    return render(request, 'auth_users/categories.html', {'items': items})


def category(request, categories):
    items = Item.objects.all().filter(category__categories=categories)
    print(items)
    return render(request, 'auth_users/category.html', {'items': items})


def profile(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'auth_users/profile.html', {'user': user})


def get_watch_list(request, pk):
    wl = Watchlist.objects.all().filter(author_id=request.user.id, watchlist=pk)
    if wl:
        return redirect('index')
    else:
        wl = Watchlist()
        wl.watchlist = pk
        wl.author_id = request.user.id
        wl.save()
        return redirect('index')


def del_watch_list(request, pk):
    Watchlist.objects.all().filter(author_id=request.user.id, watchlist=pk).delete()
    return redirect('show_watchlist')


def show_watchlist(request):
    items = []
    for wl in Watchlist.objects.all().filter(author_id=request.user.id):
        items.append(Item.objects.get(id=wl.watchlist))
    return render(request, 'auth_users/watchlist.html', {'items': items})


def search(request):
    if request.method == 'GET':
        q = request.GET['search']
        items = Item.objects.filter(title__icontains=q)
        return render(request, 'auth_users/search.html', {'items': items})


def get_cart_items(request, pk):
    ci = CartItem.objects.all().filter(author_id=request.user.id, cart_item=pk)
    if ci:
        return redirect('index')
    else:
        ci = CartItem()
        ci.cart_item = pk
        ci.author_id = request.user.id
        ci.save()
        return redirect('show_cart')


def show_cart_items(request):
    items = []
    for ci in CartItem.objects.all().filter(author_id=request.user.id):
        items.append(Item.objects.get(id=ci.cart_item))
    return render(request, 'auth_users/cart.html', {'items': items})


def del_cart_item(request, pk):
    CartItem.objects.all().filter(author_id=request.user.id, cart_item=pk).delete()
    return redirect('show_cart')
