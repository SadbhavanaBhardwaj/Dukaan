from django.contrib import admin

# Register your models here.
from .models import Owner, Store, Category

admin.site.register(Owner)
admin.site.register(Store)
admin.site.register(Category)