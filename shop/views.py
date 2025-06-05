from django.shortcuts import render
from rest_framework.decorators import api_view
<<<<<<< HEAD
from .models import Product
=======
from .models import Product, Category
from django.contrib.auth.decorators import login_required
>>>>>>> b2ee892 (ui issues solved)
from .serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.

def Home(request):
<<<<<<< HEAD
    return render(request, "home.html")

def ProductsView(request):
    return render(request, "ProductsView.html")
=======
    products= Product.objects.all()
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
        'categories': categories
    }
    return render(request, "Productslist.html", context)

@login_required
def ProductsView(request,slug):
    products = Product.objects.get(slug=slug)
    context = {
        'products': products
    }
    return render(request, "ProductsView.html", context)
>>>>>>> b2ee892 (ui issues solved)
 
@api_view(['GET'])
def shops(request):
    products = Product.objects.all()
    serializer= ProductSerializer(products,many=True)
    return Response(serializer.data)

 

