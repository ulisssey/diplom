from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:categories>/', views.category, name='category'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('watchlist/<str:pk>', views.get_watch_list, name='watchlist'),
    path('watchlist/', views.show_watchlist, name='show_watchlist'),
    path('search/', views.search, name='search')
]
