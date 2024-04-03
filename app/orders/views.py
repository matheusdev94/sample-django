from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.http import JsonResponse


from dotenv import load_dotenv, find_dotenv

import os
import json
import qrcode
import time

from datetime import datetime, timedelta

from users.forms import RegisterAddress
from users.models import WebUser, DeliverAddress
from .models import Orders


from django.core.files.base import ContentFile


from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

load_dotenv(find_dotenv())

          
import mercadopago

ACCESS_TOKEN=os.getenv('ACCESS_TOKEN')
PIX_KEY=os.getenv('PIX_KEY')

@login_required(login_url="/users/login/")
def delete_order_view(request,id):
    if request.method=="POST":
        order = Orders.objects.get(id=id)
        order.delete()
        if 'next' in request.POST:
            return redirect(request.POST.get("next"))
        
@login_required(login_url="/users/login/")
def check_payment_status_view(request):
    # Obtenha o payment_id da requisição
    payment_id = request.POST.get('payment_id')

    # Configure o ACCESS_TOKEN do Mercado Pago
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    try:
        # Consulte o status do pagamento usando o SDK do Mercado Pago
        payment_info = sdk.payment().get(payment_id)

        # Verifique o status do pagamento
        if payment_info['status'] == 'approved':
            # O pagamento foi aprovado
            payment_status = True
        else:
            # O pagamento não foi aprovado
            payment_status = False

        # Retorne o status do pagamento como uma resposta JSON
        return JsonResponse({'payment_status': payment_status})

    except Exception as e:
        # Em caso de erro, retorne uma resposta JSON indicando o erro
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required(login_url="/users/login/")
def payment_view(request, order_id, address_id):

    try:
        sdk = mercadopago.SDK(ACCESS_TOKEN)

        request_options = mercadopago.config.RequestOptions()

        order = Orders.objects.filter(id=order_id)[0]
        timeNow = datetime.now()
        expiration_time = datetime.now() + timedelta(minutes=10)

        time_now_formatted = timeNow.strftime("%Y-%m-%dT%H:%M:%S.000-40:00")
        expiration_time_formatted = expiration_time.strftime("%Y-%m-%dT%H:%M:%S.000-40:00")
        
        print("=> now: ", time_now_formatted[:-5]+'04:00')
        print("=> exp: ", expiration_time_formatted[:-5]+'04:00')

        payment_data = {
            "transaction_amount": float(order.total),
            # 'currency': 'BRL',
            "payment_method_id": "pix",
            # "date_of_expiration": expiration_time_formatted,
            "payer": {
                "email": request.user.email,
            }
        }

        payment_response = sdk.payment().create(payment_data, request_options)
        print("expiration payment:", payment_response)
        qr_code =  payment_response["response"]['point_of_interaction']['transaction_data']['qr_code']

        qr_code_img = qrcode.make(qr_code)
        buffer = BytesIO()
        qr_code_img.save(buffer, format='PNG')
        
        print(f"""
                {payment_response['response']}
        """)


        order.qr_code_image.save('qr_code.png',InMemoryUploadedFile(buffer, None, 'qr_code.png','image/png', buffer.tell(),None))
        order.qr_code_data=qr_code
        order.save()
        
        return render(request, 'orders/orders_payment.html', {
            "order_id": order_id,
            'address_id': address_id,
            'order':order,
            'expiration_time':expiration_time_formatted,
            'payment_id': payment_response['response']['id']
        })
    except:
        print('''
              
              



              exeption
              
              
              
              
              
        
        ''')
        return render(request, 'orders/orders_payment.html', {
            "order_id": order_id,
            'address_id': address_id,
            'order':order,
            'expiration_time':None,
            'payment_id': None,
            'error':True
        })


@login_required(login_url="/users/login/")
def finalize_order_view(request, id):
    if request.method == "POST":
        pass
    else:
        email=request.user.email
        webuser = WebUser.objects.filter(email=email)[0]
        addresses = DeliverAddress.objects.filter(user_phone=webuser.phone)
        if len(addresses)>0: 
            return render(request, 'orders/orders_addresses.html', {'addresses':addresses, "order_id":id})
        else:
            return redirect(reverse('users:register_address',args=[id]))
    
    return render(request, 'orders/orders_finalize.html',{"order_id":id})


@login_required(login_url="/users/login/")
def orders_list_view(request):
    orders = Orders.objects.filter(customer_email=request.user.email)
    
    for order in orders:
        order.total_price()
    
    return render(request, 'orders/orders_list.html', {'orders': orders})

@login_required(login_url="/users/login/")
def get_order_view(request,id):
    order = Orders.objects.filter(id=id)[0]
    items=order.get_products()
    items_json=order.get_list_item()
    
    return render(request, 'orders/orders_item.html', {'order': order,'items':items,'items_json':items_json})

@login_required(login_url="/users/login/")
def add_item_view(request):    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        user_email = request.user.email
        
        order = Orders.objects.filter(customer_email=user_email)
        
        if len(order) < 1:
            user = WebUser.objects.get(email=user_email)
            new_order = Orders()
            new_order.customer_email=user.email
            new_order.customer_phone=user.phone
            new_order.products = json.dumps([])

            new_order.save()
            
        order = Orders.objects.get(customer_email=user_email)
        order.add_item(int(product_id))
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('products:list')
@login_required(login_url="/users/login/")
def remove_item_view(request):    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        user_email = request.user.email

        
        order = Orders.objects.filter(customer_email=user_email)
        
        if len(order) < 1:
            return redirect('products:list')
            
        order = Orders.objects.get(customer_email=user_email)
        order.remove_item(int(product_id))

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('products:list')
        
@login_required(login_url="/users/login/")
def delete_item_view(request):    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        user_email = request.user.email

        
        order = Orders.objects.filter(customer_email=user_email)
        
        if len(order) < 1:
            return redirect('products:list')
            
        order = Orders.objects.get(customer_email=user_email)
        order.delete_item(int(product_id))
        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('products:list')





#             order = Orders.objects.filter(id=order_id)[0]
#     print()
#     order.total_price()
#     print()
#     print()
#     print('order.total')
#     print(order.total)
#     print()
#     print()
#     srt_order = ''
#     for item in order.get_products():
#         srt_order = srt_order + str(item) + '\n'
# #     description=f"""
# # ::::: PAGAMENTO SAMPLE :::::
# # cliente: {request.user.email}
# # preço: R$ {order.total}
# # itens: 
# # --------------------
# # id |  nome | tamanho
# # --------------------
# # {srt_order}
# # --------------------
# # :::::::::::::::::::::::::::::
# # """
#     description = f"pagamento SAMPLE {PIX_KEY}"
#     print(description)
#     description = f"pagamentoSAMPLE"
#     pix = f"chave={PIX_KEY}&valor={order.total}&descricao={description}"

#     qr = qrcode.make(pix)
#     qr.save(f'./payments/{order_id}-payment_pix.png')

#     # print(qr)
    