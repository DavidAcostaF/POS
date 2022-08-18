from django.contrib import admin

from apps.products.models import Product,Cart,Sale,DetailSale

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Sale)
admin.site.register(DetailSale)