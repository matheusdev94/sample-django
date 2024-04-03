import json
from products.models import Products
from django.db import models
import PIL

class Orders(models.Model):
    id             = models.AutoField( primary_key=True)
    customer_email = models.EmailField(max_length=50, default="DEFAULT")
    customer_phone = models.CharField(max_length=50, default="DEFAULT")
    status         = models.BooleanField(max_length=50, default=False    )
    total          = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    products       = models.TextField(max_length=200, default=[])
    date           = models.DateField(auto_now_add=True)
    qr_code_data   = models.CharField(max_length=160, default="DEFAULT")
    qr_code_image  = models.ImageField(default="DEFAULT", upload_to='payments/')

    def get_list_item(self):
        if self.products:
            return json.loads(self.products)
        else:
            return []
        
    def get_products(self):
        items = self.get_list_item()
        
        prd=[]
        for item in items:
            prd.append(Products.objects.get(id=item['id']))
        return prd
    
    
    def add_item(self, id):
        items = self.get_list_item()
        item_exists = False
        
        # Verificar se o item já existe na lista
        for item in items:
            if item['id'] == id:
                if item['quantity'] >= 20:
                    return
                item['quantity'] += 1
                item_exists = True
                break
            
        # Se o item não existe na lista, adicionar um novo
        if not item_exists:
            items.append({'id': id, 'quantity': 1})
        
        # Atualizar a lista de itens no objeto de pedido
        self.products = json.dumps(items)
        
        # Set the total price before saving

        self.total = self.total_price()
        self.save()
        
    def delete_item(self, id):
        items = self.get_list_item()
        # items.pop(id)
        filtered_list = []
        for item in items:
            if item['id'] != id:
                filtered_list.append(item)
        
        self.products = json.dumps(filtered_list)
        self.total = self.total_price()

        self.save()
    
    def remove_item(self, id):
        items = self.get_list_item()
        item_exists = False

        # Verificar se o item já existe na lista
        for item in items:
            if item['id'] == id:
                if item['quantity'] <= 0:
                    return
                item['quantity'] -= 1
                item_exists = True
                break
        # Se o item não existe na lista, adicionar um novo
        if not item_exists:
            items.append({'id': id, 'quantity': 1})
        # Atualizar a lista de itens no objeto de pedido
        self.products = json.dumps(items)
        self.total = self.total_price()
        self.save()
    
    def total_price(self):
        items = self.get_list_item()
        if len(items) <= 0:
            self.total = 0
            self.save()
            return 0

        total_sum = 0
        for item in items:
            prd = Products.objects.get(id=item['id'])
            total_sum = total_sum + prd.price * item['quantity']
        self.total = total_sum
        self.save()
        return total_sum

    def __str__(self) -> str:
        return f'Pedido #{self.id} | STATUS (pago): {self.status} | Nome: {self.customer_email} | Phone: {self.customer_phone}'

