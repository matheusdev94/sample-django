from django.db import models
from PIL import Image

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    slug = models.SlugField(max_length=50)
    banner = models.ImageField(upload_to='pics/', default='fallback.png')


    def __str__(self):
        return f'{self.id} - {self.name} - {self.size}'
class Photo(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='pics/')


    
    # resizing the image, you can change parameters like size and quality.
    def save(self, *args, **kwargs):
       super(Photo, self).save(*args, **kwargs)
       img = Image.open(self.photo.path)
       if img.height > 1125 or img.width > 1125:
           img.thumbnail((1125,1125))
       img.save(self.photo.path,quality=70,optimize=True)

# # Create your models here.
# class Order(models.Model):
#     # user       = models.CharField(max_length=100)
#     id = models.AutoField(primary_key=True)
#     total          = models.CharField(max_length=100)
#     customer_name  = models.CharField(max_length=100)
#     customer_phone = models.CharField(max_length=100)
#     products       = models.ManyToManyField(Products)
#     date           = models.DateField(auto_now_add=True)

#     def total_price(self):
#         return sum(product.price for product in self.products.all())
#     def __str__(self) -> str:
#         return f'Pedido #{self.id} - Nome: {self.customer_name} | Phone: {self.customer_phone}'

