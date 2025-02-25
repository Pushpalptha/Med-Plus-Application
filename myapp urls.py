from django.urls import path
from . import views 
app_name = 'myapp' 
urlpatterns = [
    path('login/', views.ulogin, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.ulogout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/medications/', views.medication_list, name='medication_list'),
    path('medications/<int:medication_id>/', views.medication_detail, name='medication_detail'),
    path('search/',views.search_category,name='search'),
    path('cart/<int:medication_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
 
