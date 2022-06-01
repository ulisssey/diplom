import datetime

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Item, Categories, Watchlist, OrderItem, Order, Address


import stripe


endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    items = Item.objects.all()
    p = Paginator(items, 6)
    page_num = request.GET.get('page', '1')
    page = p.page(page_num)
    nums = [x for x in range(1, p.num_pages+1)]
    return render(request, 'auth_users/base.html', {'items': page, 'nums': nums})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        if password1 == password2:
            User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password1)
        user = authenticate(username=username, password=password1)
        login(request, user)
        return redirect('index')
    return render(request, 'auth_users/register.html')


@csrf_exempt
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
    return render(request, 'auth_users/categories.html')


def category(request, categories):
    items = Item.objects.all().filter(category__categories=categories)
    p = Paginator(items, 4)
    page_num = request.GET.get('page', '1')
    page = p.page(page_num)
    nums = [x for x in range(1, p.num_pages + 1)]
    title = items[0].category
    return render(request, 'auth_users/category.html', {'items': page, 'nums': nums, 'category': title})


def itempage(request, pk):
    item = Item.objects.filter(id=pk).first()
    return render(request, 'auth_users/item-page.html', {'item': item})


@login_required(login_url='login')
@csrf_exempt
def profile(request, pk):
    user = User.objects.get(id=pk)
    address = Address.objects.filter(user=request.user).first()
    context = {'user': user}
    if address is not None:
        context['address'] = address
    if request.method == 'POST':
        city = request.POST.get('city')
        street = request.POST.get('street')
        apartment = request.POST.get('apartment')
        if address is None:
            address = Address(user=request.user, city=city, street_address=street, apartment=apartment)
            address.save()
        else:
            address.city = city
            address.street_address = street
            address.apartment = apartment
            address.save()
    return render(request, 'auth_users/profile.html', context)


@login_required(login_url='login')
@csrf_exempt
def changeprofile(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        user = User.objects.filter(id=request.user.id).first()
        if len(firstname) != 0:
            user.first_name = firstname
        if len(lastname) != 0:
            user.last_name = lastname
        if len(email) != 0:
            user.email = email
        user.save()
        return redirect('profile', user.id)
    return render(request, 'auth_users/edit-profile.html')


@login_required(login_url='login')
@csrf_exempt
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


@login_required(login_url='login')
@csrf_exempt
def del_watch_list(request, pk):
    Watchlist.objects.all().filter(author_id=request.user.id, watchlist=pk).delete()
    return redirect('show_watchlist')


@login_required(login_url='login')
def show_watchlist(request):
    items = []
    for wl in Watchlist.objects.all().filter(author_id=request.user.id):
        items.append(Item.objects.get(id=wl.watchlist))
    p = Paginator(items, 6)
    page_num = request.GET.get('page', '1')
    page = p.page(int(page_num))
    nums = [x for x in range(1, p.num_pages + 1)]
    return render(request, 'auth_users/watchlist.html', {'items': page, 'nums': nums})


def search(request):
    if request.method == 'GET':
        q = request.GET['search']
        items = Item.objects.filter(title__icontains=q)
        return render(request, 'auth_users/search.html', {'items': items})


@login_required(login_url='login')
def add_to_cart(request, pk):
    ordered_date = timezone.now()
    item = Item.objects.get(id=pk)
    order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False).first()
    if order_item is None:
        order_item = OrderItem(user=request.user, item=item, ordered=False)
        order_item.save()
    else:
        order_item.quantity += 1
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order is not None:
        order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('show_cart')


@login_required(login_url='login')
def show_cart(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    return render(request, 'auth_users/cart.html', {'object': order})


def increase_quantity(request, pk):
    item = Item.objects.get(id=pk)
    order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False).first()
    order_item.quantity += 1
    order_item.save()
    return redirect('show_cart')


def decrease_quantity(request, pk):
    item = Item.objects.get(id=pk)
    order_item = OrderItem.objects.filter(user=request.user, item=item, ordered=False).first()
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


@csrf_exempt
def create_checkout_session(request):
    order_id = request.POST.get('order-id')
    order = Order.objects.filter(id=order_id).first()
    names = []
    for order_item in order.items.all():
        names.append(order_item.item.title)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency': 'kzt',
                        'unit_amount': order.get_total()*100,
                        'product_data': {
                            'name': ', '.join(names),
                        },
                    },
                    'quantity': 1,
                },
            ],
        metadata={
            "order_id": order_id,
            "email": order.user.email
        },
        phone_number_collection={
            'enabled': True,
        },
        customer_email=order.user.email,
        mode='payment',
        success_url='http://127.0.0.1:8000/' + 'success/',
        cancel_url='http://127.0.0.1:8000/' + 'cancel/',
    )
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.payment_status == 'paid':
            # Fulfill the purchase...
            order_id = session['metadata']['order_id']
            print(session)
            fulfill_order(order_id)
            send_mail(
                'Тауарды сатып алуыңызбен құтықтаймыз!',
                'рахмет',
                settings.EMAIL_HOST_USER,
                [session['metadata']['email']]
            )
    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(order_id):
    order = Order.objects.filter(id=order_id).first()
    order_item = order.items.all()
    order.ordered = True
    order.ordered_date = datetime.datetime.now()
    for item in order_item:
        item.ordered = True
        item.save()
    order.shipping_address = Address.objects.filter(user=order.user).first()
    order.save()
    print("Fulfilling order")


def success(request):
    return redirect('index')


def cancel(request):
    return render(request, 'auth_users/cancel.html')


def slider(request):
    return render(request, 'auth_users/slider.html')