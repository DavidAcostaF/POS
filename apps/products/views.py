from django.http import HttpResponse,HttpResponseRedirect 
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,TemplateView,View,ListView,DeleteView,UpdateView,DetailView
from django.db.models import Sum,F,Q
from pathlib import Path
from django.conf import settings
from django.template.loader import get_template
import pdfkit
from django.template import loader
import csv
import platform
from django.core.mail import EmailMessage
from django.contrib import messages
# Create your views here.

from . import models
from . import forms
from apps.users.mixins import LoginMixins


# class base(LoginMixins,ListView):
#     model = models.Car
#     template_name = 'base.html'
#     # context_object_name = 'product_list'

#     def get_queryset(self):
#         user = self.request.user
#         context = models.Car.objects.filter(user = user)
#         return context

def MyCar(request):
    user = request.user
    if user.is_authenticated:
        products = models.Cart.objects.filter(user = request.user)
        total = models.Cart.objects.filter(user = request.user).aggregate(total = Sum('quantity'))
        context = {
                'products':products,
                'total':total
            }
        return context
    else:
        context = {
                'products':models.Cart.objects.none(),
                'total':'total'
            }
        return context

class CreateProduct(CreateView):
    model = models.Product
    form_class = forms.FormProducts
    template_name = 'inventory/add_products.html'
    success_url = reverse_lazy('create_products')

class ProductsInventory(ListView):
    model = models.Product
    template_name = 'inventory/stock_inventory.html'

    def get_queryset(self):
        product = self.model.objects.filter(state = True)
        return product


class ProductsList(ListView):
    model = models.Product
    template_name = 'products/products_stock.html'
    
    def get_queryset(self):
        product = self.model.objects.filter(state = True, stock__gt=0)
        return product

class DeleteInventory(DeleteView):
    model = models.Product
    success_url = reverse_lazy('products_inventory')

class UpdateInventory(UpdateView):
    model = models.Product
    form_class  = forms.FormProducts
    template_name = 'inventory/update_inventory.html'
    success_url = reverse_lazy('products_inventory')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddToCart(View):
    model = models.Cart
    success_url = reverse_lazy('products_lists')
    
    def post(self,request,pk):
        user = request.user
        product = models.Product.objects.get(id = pk)
        add,created = self.model.objects.get_or_create(user = user, product = product)
        if not created:
            if add.quantity < product.stock:
                add.quantity += 1
                add.save()
        return redirect(self.success_url)

class Cart(ListView):
    model = models.Cart
    template_name = 'products/car.html'

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.filter(user = user)
        return queryset

class UpdateQuantity(UpdateView):
    model = models.Cart

    def post(self,request,pk):
        product = self.get_object()
        quantity = int(request.POST.get('quantity'))
        if quantity >= 1:
            if quantity <= product.product.stock:
                product.quantity = quantity
                product.save()
        else:
            product.delete()
        return HttpResponse(status = 204)

class Buy(View):
    model = models.DetailSale
    success_url = reverse_lazy('products_lists')

    def post(self,request):
        user = request.user
        products = models.Cart.objects.filter(user = user)

        if products:
            for item in products:
                total = item.product.price*item.quantity
                create = self.model.objects.create(user = user, product = item.product,quantity = item.quantity,total=total)
                create.save()
                item.product.stock = item.product.stock - item.quantity
                item.product.save()
            products.delete()
            models.Sale.objects.create(user = user)
        return redirect(self.success_url)


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'products/detail_product.html'
    context_object_name = 'product'
    def get_object(self,**kwargs):
        return self.model.objects.get(name = self.kwargs['name'])

class AddToCartWithQuantity(View):
    model = models.Cart

    def post(self,request,pk,**kwargs):
        user = request.user
        product = models.Product.objects.get(id = pk)
        quantity = int(request.POST.get('input'))
        add,created = self.model.objects.get_or_create(user = user, product = product)
        if not created and add.quantity < product.stock:
            # if add.quantity < product.stock:
            if add.quantity >= product.stock:
                add.quantity = product.stock
                add.save()
            else:
                add.quantity += quantity
                add.save()
        else:
            add.quantity = quantity
            add.save()
        return redirect('product_detail', name=product)


class PurchaseHistory(ListView):
    model = models.DetailSale
    template_name = 'products/purchase_history.html'
    context_object_name = 'history'

    def get_queryset(self):
        user = self.request.user
        context = self.model.objects.filter(user = user)
        return context


class TotalSales(ListView):
    model = models.DetailSale
    template_name = 'inventory/total_sales.html'
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        objects = self.model.objects.all()
        total = self.model.objects.all().aggregate(total = Sum('total'))
        data['objects'] = objects
        data['total'] = total
        return data


def get_data(request):

    info = models.DetailSale.objects.all()
    total = models.DetailSale.objects.all().aggregate(total = Sum('total'))
    data = {
        'info':info,
        'total':total
    }

    return data

def get_absolute_path():
    return Path(__file__).parent.resolve()

def generate_pdf(request,template_name = 'inventory/pdf.html'):
    data = get_data(request = request)
    template = get_template(template_name)
    html = template.render(data)
    options = {
        "page-size": 'Letter', # Page size 
        'title': 'Total Sales', # File title
        'margin-top': '200px', # Margin top
        'margin-right': '0px', # Margin right
        'margin-left': '0px', # Margin left
        'margin-bottom': '10px', # Margin botton
        'encoding': "ISO-8859-3", # File enconding, it can be UTF-8 but sometimes it does not work
        # 'footer-html': 'templates/footer.html', # Footer
        # '--header-html': 'templates/header.html', # Header
        '--header-spacing': '-223', # Header spacing from the content
        '--footer-spacing': '-14', # Footer spacing from the content
        '--enable-local-file-access': "", # The pdf can access file from the local machine
    }

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf') \
        if platform.system() != 'Windows' \
        else pdfkit.configuration(
            # Windows config
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    css = [
        f'{settings.STATICFILES_DIRS[0]}/assets/css/style.css', 
        f'{settings.STATICFILES_DIRS[0]}/assets/vendor/bootstrap/css/bootstrap.min.css',
    ]

    # html, options=options, configuration=config, css=css
    pdf_file = pdfkit.from_string(html,options = options,configuration = config,css=css)
    return pdf_file

class CreatePdf(View):
    def get(self,request):
        return HttpResponse(generate_pdf(request),content_type='application/pdf',headers={'Content-Disposition': 'attachment; filename="total_sales.pdf"'})


class FilterProducts(ListView):
    model = models.Product
    template_name = 'products/products_stock.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.get('query')
        query = self.model.objects.filter(Q(name__icontains = params) | Q(description__icontains = params))
        context['object_list'] = query
        return context



def generate_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="totalsales.csv"'},
    )

    info = models.DetailSale.objects.all()
    total = models.DetailSale.objects.all().aggregate(total = Sum('total'))
    
    csv_data = {
        'info':info,
        'total':total
    }
    print(csv_data)
    template = loader.get_template('convert/csv.txt')
    response.write(template.render(csv_data))
    return response

class CreateCsv(View):

    def get(self,request):
        return HttpResponse(generate_csv(request),content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="total_sales.csv"'})

class DeleteInCart(DeleteView):
    model = models.Cart
    success_url = reverse_lazy('products_lists')


def EmailPdf(request):
    email = EmailMessage(
        'Total Sales',
        'Total Sales',
        settings.EMAIL_HOST_USER,
        [request.user.email],
        )
    email.attach("totalsales.pdf",generate_pdf(request))
    email.fail_silently = False
    email.send()

    messages.success(request,'Email Sent')
    return redirect('total_sales')


