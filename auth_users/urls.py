from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create-checkout-session', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/stripe', views.my_webhook_view, name='webhook-stripe'),

    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('categories/', views.categories, name='show_categories'),
    path('categories/<str:categories>/', views.category, name='category'),
    path('item-page/<str:pk>', views.itempage, name='item-page'),

    path('profile/<str:pk>', views.profile, name='profile'),
    path('edit-profile', views.changeprofile, name='edit-profile'),
    path('slider', views.slider),
    path('order/<str:pk>', views.order, name='order'),

    path('add-watchlist/<str:pk>', views.get_watch_list, name='add-watchlist'),
    path('delete-watchlist/<str:pk>', views.del_watch_list, name='del-watchlist'),
    path('watchlist', views.show_watchlist, name='show_watchlist'),

    path('search/', views.search, name='search'),

    path('add-item/<str:pk>', views.add_to_cart, name='add-cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('increase/<str:pk>', views.increase_quantity, name='increase-q'),
    path('decrease/<str:pk>', views.decrease_quantity, name='decrease-q'),
    path('delete-item/<str:pk>', views.delete_single_item, name='delete-item'),

]
