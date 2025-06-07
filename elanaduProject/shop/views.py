from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from .serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.

def Home(request):
    products = Product.objects.all().order_by('-id')[:6]

    context = {
        'products': products
    }
    return render(request, "home.html",context)

@login_required
def Productslist(request):
    products= Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        
    }
    return render(request, "Productslist.html", context)

@login_required
def ProductsView(request,slug):
    products = Product.objects.get(slug=slug)
    context = {
        'products': products
        
    }
    return render(request, "ProductsView.html", context)
 
 
# @api_view(['GET'])
# def shops(request):
#     products = Product.objects.all()
#     serializer= ProductSerializer(products,many=True)
#     return Response(serializer.data)

 

@login_required
def filterCategory(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category.name   
    }
    return render(request, "Productslist.html", context)
