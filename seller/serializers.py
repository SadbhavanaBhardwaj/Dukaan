from .models import Owner, Store, Category
from buyer.models import Customer, ItemDetails, Cart
from rest_framework import serializers

class OwnerSerializer(serializers.ModelSerializer):

    otp = serializers.CharField(max_length=5, read_only=True)
    phone_number = serializers.CharField(source='username')
    
    class Meta():
        model = Owner
        fields = ['otp', 'phone_number']

    def validate(self, attrs):
        attrs.update({'password': ''})
        #attrs.update({'username':attrs['phone_number']})
        return attrs

class StoreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    class Meta():
        model = Store
        fields = ['id', 'slug', 'address', 'store_name']


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')
    class Meta():
        model = Category
        fields = ['category_name']

