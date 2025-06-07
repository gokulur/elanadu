from django.urls import path
from .import views

urlpatterns = [
    path('',views.Home,name='Home'),
    # path('products',views.shops,name='shops'),
    path('Products',views.Productslist,name='ProductsView'),
    path('product/<slug:slug>/', views.ProductsView, name='product_detail'),
    path('category/<slug:slug>/', views.filterCategory, name='filterCategory'),

]