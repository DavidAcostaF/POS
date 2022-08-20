from django.urls import path
from apps.products import views

urlpatterns = [
    path('create_products/',views.CreateProduct.as_view(),name='create_products'),
    path('products_inventory/',views.ProductsInventory.as_view(),name='products_inventory'),
    path('delete_inventory/<int:pk>',views.DeleteInventory.as_view(),name='delete_inventory'),
    path('update_inventory/<int:pk>',views.UpdateInventory.as_view(),name='update_inventory'),
    path('add_cart/<int:pk>',views.AddToCart.as_view(),name='add_car'),
    path('update_quantity/<int:pk>',views.UpdateQuantity.as_view(),name='update_quantity'),
    path('buy/',views.Buy.as_view(),name='buy'),
    path('product_detail/<str:name>/',views.ProductDetail.as_view(),name='product_detail'),
    path('add_with_quantity/<int:pk>',views.AddToCartWithQuantity.as_view(),name='add_with_quantity'),
    path('purchase_history/',views.PurchaseHistory.as_view(),name='purchase_history'),
    path('total_sales/',views.TotalSales.as_view(),name='total_sales'),
    path('products_lists/',views.FilterProducts.as_view(),name='filter_products'),
    path('pdf_file/',views.CreatePdf.as_view(),name='pdf_file'),
    path('create_csv/',views.CreateCsv.as_view(),name='create_csv'),
    path('delete_in_cart/<int:pk>',views.DeleteInCart.as_view(),name='delete_in_cart'),
    path('email_pdf',views.EmailPdf,name='email_pdf')
]