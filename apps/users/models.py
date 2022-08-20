from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin



# Create your models here.

class MyUserManager(BaseUserManager):
    def _create_user(self,email,first_name,last_name,password,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email,first_name,last_name,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,first_name,last_name,password,**extra_fields)

    def create_superuser(self,email,first_name,last_name,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email,first_name,last_name,password,**extra_fields)

class MyUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    country = models.CharField(max_length=200,null = True,blank=True)
    address = models.CharField(max_length=200,null = True,blank=True)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='profile')
    uuid = models.CharField(null= True,blank=True,max_length=10)
    activate = models.BooleanField(default=False)
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'







