from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.

def Home(request):
    return render(request, "home.html")

def ProductsView(request):
    return render(request, "ProductsView.html")
 
@api_view(['GET'])
def shops(request):
    products = Product.objects.all()
    serializer= ProductSerializer(products,many=True)
    return Response(serializer.data)

 

