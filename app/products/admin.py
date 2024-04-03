from django.contrib import admin
from .models import Products, Photo
# Register your models here.
# admin.site.register(Products)

class PhotoAdmin(admin.StackedInline):
    model = Photo

class ProductsAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin]
    class Meta:
        model = Products

admin.site.register(Photo)
admin.site.register(Products, ProductsAdmin)
