from django.shortcuts import render
from .models import Products, Photo
from django.http import HttpResponse

def get_products_list(request):
    products = Products.objects.all()
    photos = Photo.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'photos': photos})


def get_product(request, slug):
    product = Products.objects.get(slug=slug)
    photos = Photo.objects.filter(product=product)
    
    return render(request,'products/product_item.html', {'product': product, 'photos': photos})
