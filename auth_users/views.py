from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import UserForm
from .models import Item, Categories, Watchlist, OrderItem, Order


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


def add_to_cart(request, pk):
    ordered_date = timezone.now()
    item = Item.objects.get(id=pk)
    order_item = OrderItem(user=request.user, item=item, ordered=False)
    order_item.save()
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('/')


def show_cart(request):
    order = Order.objects.get(user=request.user, ordered=False)
    return render(request, 'auth_users/cart.html', {'object': order})


def increase_quantity(request, pk):
    item = Item.objects.get(id=pk)
    order_item = OrderItem.objects.filter(user=request.user, item=item).first()
    order_item.quantity += 1
    order_item.save()
    return redirect('show_cart')


def decrease_quantity(request, pk):
    item = Item.objects.get(id=pk)
    order_item = OrderItem.objects.filter(user=request.user, item=item).first()
    if order_item.quantity > 0:
        order_item.quantity -= 1
        order_item.save()
    return redirect('show_cart')


def delete_single_item(request, pk):
    item = Item.objects.get(id=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item=item).exists():
            order_item = OrderItem.objects.filter(
                user=request.user, ordered=False, item=item
            )[0]
            order.items.remove(order_item)
            OrderItem.objects.filter(user=request.user, ordered=False, item=item).delete()
    return redirect('show_cart')
