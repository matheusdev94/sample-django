from django.contrib import admin
from .models import WebUser, DeliverAddress

# Register your models here.
admin.site.register(WebUser)
admin.site.register(DeliverAddress)