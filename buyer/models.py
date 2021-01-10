from django.db import models
from django.core import validators
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib import auth
from random import randint
from django.utils.text import slugify
from seller.models import Category, Store

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    mrp = models.PositiveIntegerField()
    sales_price = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class Cart(models.Model):
    store_link = models.CharField(max_length=255)


class ItemDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

class Customer(auth.models.User):
    address = models.CharField(max_length=500)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)