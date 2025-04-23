from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    contact=models.CharField(max_length=20,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Link the custom user manager
    objects = CustomUserManager()

    # Set the unique identifier to be the email field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # You can add extra required fields here

    def __str__(self):
        return self.email
    



class Category(models.Model):
    name=models.CharField(max_length=255)
    img=models.ImageField(upload_to='Category', default='', null=True)
    choice=(('Active', 'Active'),('Disable','Disable'),)
    status=models.CharField(max_length=255,choices=choice)

    def __str__(self):
        return self.name


class Brands(models.Model):
    name=models.CharField(max_length=255)
    img=models.ImageField(upload_to='Brands', default='',null=True)
    choice=(('Active','Active'),('Disable','Disable'),)
    status=models.CharField(max_length=255,choices=choice)

    def __str__(self):
        return self.name
    

class Products(models.Model):
    title=models.CharField(max_length=255 , null=True)
    name=models.CharField(max_length=255)
    brand=models.ForeignKey(Brands,on_delete=models.CASCADE, null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    description=models.TextField()
    price=models.CharField(max_length=100)
    discount=models.CharField(max_length=100)
    pcode=models.CharField(max_length=255)
    img=models.ImageField(upload_to='Products', default='', null=True)
    stock=models.CharField(max_length=255)
    choice=(('Active','Active'),('Disable','Disable'),)
    status=models.CharField(max_length=255,choices=choice)
    tchoice=(('Yes','Yes'),('No','No'),)
    tstatus=models.CharField(max_length=255,choices=tchoice)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    cart_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    wish_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty=models.IntegerField()
    orderid=models.CharField(max_length=100)
    orderdate=models.DateField(auto_now_add=True)
    ordertrans=(('Success','Success'),
                ('Pending','Pending'),
                ('Delivered','Delivered'),
                ('Cancelled','Cancelled'),
                ('Return','Return'),
                ('Refund','Refund'))
    status=models.CharField(max_length=150,choices=ordertrans)

    def __str__(self):
        return self.orderid
    

class Billing(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    orderid=models.ForeignKey(Order,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    email=models.EmailField()
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=30)
    amount=models.CharField(max_length=255)
    choice=(('Online','Online'),('COD','COD'))
    payment_mode=models.CharField(max_length=255,choices=choice)
    billing_date=models.DateField(auto_now_add=True)  


    def __str__(self):
        return self.first_name 