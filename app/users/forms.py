from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms 
from django.contrib.auth.models import User
from .models import WebUser, DeliverAddress
from .regex import Regex

class RegisterAddress(forms.ModelForm):
    cep                = forms.CharField(max_length=8, validators=[Regex.cep_regex], widget=forms.TextInput(attrs={'id':'id_cep', 'max':'99999999'}), label="CEP")
    street             = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly': 'readonly', 'id':'id_street'}), label="Rua")
    uf                 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly': 'readonly', 'id':'id_uf'}), label="UF")
    city               = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly': 'readonly', 'id':'id_city'}), label="Cidade")
    name               = forms.CharField(max_length=50,validators=[Regex.name_regex],help_text="Esse campo ajuda a identificar o endereço. </br>Exemplo: Casa ou Trabalho.")
    address_number     = forms.CharField(max_length=7, validators=[Regex.address_number_regex], label="Nº")
    address_complement = forms.CharField(max_length=20, label="Complemento", required=False)
    user_phone         = forms.CharField(max_length=9, label="Telefone", required=True, help_text="Nº de contato.")
    # user_email         = forms.EmailField(max_length=60, widget=forms.TextInput(attrs={'readonly': 'readonly', 'id':'id_email_address_registration'}), label="Email")

    class Meta:
        model = DeliverAddress
        fields = (
            'cep', 
            'street', 
            'city', 
            'uf',
            'address_number', 
            'address_complement', 
            'name',
            'user_phone',
        )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user_email'].widget = forms.HiddenInput()

class CustomerRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=9, label='Telefone', validators=[Regex.phone_regex])

    class Meta(UserCreationForm):
    
        model = User
        fields = ( 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'phone', 
            'password1', 
            'password2'
        )

    def __init__(self,*args,**keyargs):
        super().__init__(*args,**keyargs)
        self.fields['username'].widget = forms.HiddenInput()
