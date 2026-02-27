from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('', views.product_list, name='products'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('category/<slug:category_slug>/', views.product_list, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.all_categories, name='all_categories'),
    path('search/', views.product_search, name='product_search'),
    path('home/', views.home, name='home'),
    
]