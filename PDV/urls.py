"""PDV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from apps.products.views import ProductsList
from apps.users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ProductsList.as_view(),name='products_lists'),
    path('products/',include('apps.products.urls')),
    path('accounts/login/',views.Login.as_view(),name = 'login'),
    path('accounts/register/',views.Register.as_view(),name = 'register'),
    path('accounts/logout/',views.UserLogout,name = 'logout'),
    path('accounts/profile/',views.Profile.as_view(),name='profile'),
    path('accounts/change_password/',views.UpdatePassword.as_view(),name='update_password'),
    path('accounts/activate/<str:slug>/',views.Activate.as_view(),name='activate'),
    path('accounts/activate_mail/',views.Resend.as_view(),name='activate_mail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
