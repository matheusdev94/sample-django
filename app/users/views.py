from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponse

from .forms import CustomerRegistrationForm, RegisterAddress
from .models import WebUser, DeliverAddress

@login_required(login_url="/users/login/")
def register_address_view(request, order_id):
    if request.method == "POST": 
        form = RegisterAddress(request.POST)
        
        if form.is_valid():
            # Process the form data and save the address
            # Assuming you have code here to save the address
            form.save()
            # if 'next' in request.POST:
            #     return redirect(request.POST.get('next'))
            # else:
            # return redirect("{% url 'orders:finalize_order/<int:id>/'%}")
            # return redirect(reverse('orders:finalize_order/',args=[order_id]))
            return redirect(reverse('orders:finalize_order', args=[order_id]))
        else:
            # return redirect(reverse('orders:finalize_order', args=[order_id]))
            return redirect(reverse('users:register_address',args=[order_id]))
    else:
        form = RegisterAddress()
        return render(request, 'users/address.html', {'form': form, "order_id":order_id})
    
def register_view(request):
    if request.method == "POST":
        form_users = CustomerRegistrationForm(request.POST)
        user = WebUser()
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')

        if form_users.is_valid():
            form_users.save()
            user.save()
            login(request, form_users.save())
            if User.objects.get(email=user.email):
                # return HttpResponse('logado')
                return redirect("products:list")
            else:
                return redirect("users:register")
    else: 
        form = CustomerRegistrationForm()
        return render(request,'users/register.html',{"form": form})

def login_view(request):
    if request.method == "POST": 
        form = AuthenticationForm(data = request.POST) 
        if form.is_valid(): 
            # LOGIN HERE
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('products:list')
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')