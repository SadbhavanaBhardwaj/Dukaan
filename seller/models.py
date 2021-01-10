from django.db import models
from django.core import validators
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib import auth
from random import randint
from django.utils.text import slugify


class Owner(auth.models.User):  #change to accounts
    pass

    
class Store(models.Model):
    store_name = models.CharField(max_length=256, null=False, blank=False)
    address = models.CharField(max_length=500, null=False, blank=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if Store.objects.filter(store_name=self.store_name).exists():
            extra = str(randint(1, 10000))
            self.slug = slugify(self.store_name) + "-" + extra
        else:
            self.slug = slugify(self.store_name)
        super(Store, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=255, default="New")


