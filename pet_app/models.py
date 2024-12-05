from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False, verbose_name="Is admin")
    is_user = models.BooleanField(default=False, verbose_name="Is User")
    is_expert = models.BooleanField(default=False, verbose_name="Is Expert")
    is_seller = models.BooleanField(default=False, verbose_name="Is Seller")
    is_shop = models.BooleanField(default=False, verbose_name="Is Shop  ")
    name = models.CharField(max_length=100,null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=20,null=True, blank=True)
    role = models.CharField(max_length=20,null=True, blank=True)
    photo = models.ImageField(upload_to='profile/',null=True, blank=True)

        

class Category(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=100,null=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='pet/',null=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    description =models.CharField(max_length=300,null=False)
    breed=models.CharField(max_length=200,null=False)
    color=models.CharField(max_length=100,null=False)
    stock_level=models.IntegerField(null=False)
    age=models.CharField(max_length=100,null=False)
    vaccination = models.CharField(max_length=300,null=True)
    

class Products(models.Model):
    SHOP = models.ForeignKey(User, on_delete=models.CASCADE)
    name =models.CharField(max_length=100,null=False)    
    category =models.ForeignKey(Category,on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='product/',null=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True) 
    description = models.CharField(max_length=300,null=False)
    stock_level =models.IntegerField(null=False)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.content_object.price

    def __str__(self):
        return f"{self.quantity} x {self.content_object}"    
    
class BookingTable(models.Model):
    Date = models.DateField()
    Status = models.CharField(max_length=20)
    Total = models.FloatField()
    USER = models.ForeignKey(User, on_delete=models.CASCADE)


class BookingDetails(models.Model):
    Quantity = models.IntegerField()
    Status = models.CharField(max_length=30)
    PRODUCT = models.ForeignKey(Products, on_delete=models.CASCADE)
    BOOK = models.ForeignKey(BookingTable, on_delete=models.CASCADE)

class AssignTable(models.Model):
    BOY = models.ForeignKey(User, on_delete=models.CASCADE)
    BOOKING = models.ForeignKey(BookingDetails, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Status = models.CharField(max_length=30, blank=True, null=True)
    Comments = models.CharField(max_length=500, blank=True, null=True)  

class memberaccount(models.Model):
    id=models.AutoField(primary_key=True)
    account_number=models.CharField(max_length=50)
    IFSC=models.CharField(max_length=50)
    key=models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    member = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def _str_(self):
        return str(self.member)