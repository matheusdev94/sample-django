from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('',                                         views.orders_list_view,          name='orders_list'),
    path('add_item/',                                views.add_item_view,             name='add_item'),
    path('remove_item/',                             views.remove_item_view,          name='remove_item'),# i.e: decrease item
    path('delete_item/',                             views.delete_item_view,          name='delete_item'),
    path('<int:id>/',                                views.get_order_view,            name='order'),
    path('check_payment/',                           views.check_payment_status_view, name='check_payment'),
    path('delete_order/<int:id>/',                   views.delete_order_view,         name='delete_order'),
    path('payment/<int:order_id>/<int:address_id>/', views.payment_view,              name='payment'),
    path('finalize_order/<int:id>/',                 views.finalize_order_view,       name='finalize_order'),
]
