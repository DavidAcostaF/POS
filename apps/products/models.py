from django.db import models

from apps.users.models import MyUser

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to = 'products')
    stock = models.IntegerField()
    price = models.IntegerField()
    state = models.BooleanField(default = True)
    create_date = models.DateField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return f'{self.name}'

class Cart(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.quantity*self.product.price

class Sale(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now=True,auto_now_add=False)

class DetailSale(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    total = models.IntegerField()
    buy_date = models.DateField(auto_now=True,auto_now_add=False)

    def subtotal(self):
        return self.quantity*self.product.price