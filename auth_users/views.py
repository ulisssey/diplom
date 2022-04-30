from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import Item, Categories


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
