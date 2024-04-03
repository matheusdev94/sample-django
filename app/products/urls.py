from django.urls import path

from . import views

app_name='products'

urlpatterns = [
    path('',views.get_products_list, name='list'),
    # path('create_order',views.create_order, name='create_order'),
    path('<slug:slug>',views.get_product, name='product'),
]
