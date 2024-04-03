from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from .regex import Regex

class WebUser(AbstractBaseUser):
    phone = models.CharField(max_length=9, validators=[Regex.phone_regex])
    phone_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, validators=[Regex.name_regex], default="NONAME")
    last_name = models.CharField(max_length=50, validators=[Regex.name_regex], default="NONAME")
    email = models.EmailField(max_length=60)
    
    password = None
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone} "
    
class DeliverAddress(models.Model):
    id                 = models.AutoField(primary_key=True)
    name               = models.CharField(max_length=20,validators=[Regex.name_regex], default="Casa")
    cep                = models.CharField(max_length=8, validators=[Regex.cep_regex])
    street             = models.CharField(max_length=50)
    city               = models.CharField(max_length=50)
    uf                 = models.CharField(max_length=50)
    address_number     = models.CharField(max_length=7, validators=[Regex.address_number_regex])
    address_complement = models.CharField(max_length=20, blank=True, null=True)
    user_phone         = models.CharField(max_length=9)
    user_email         = models.EmailField(max_length=60,blank=True, null=True)

    def __str__(self):
        # return f'Local: {self.name} - CEP: {self.cep} - Telefone: {self.user_phone} '
        return f'Local: {self.name} - CEP: {self.cep} - Telefone: {self.user_phone}'