from django.urls import path,include
from .import views

urlpatterns = [
    path('products',views.shops,name='shops'),
    
]