from .models import Product, Customer, ItemDetails, Cart
from rest_framework import serializers
from seller.serializers import CategorySerializer
from seller.models import Category

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta():
        model = Product
        fields = ['id', 'product_name', 'description', 'mrp', 'sales_price', 'image', 'category', 'store']

    def create(self, validated_data):
        print(validated_data['category'])
        c, _ = Category.objects.get_or_create(name=validated_data['category']['name'])
        validated_data.pop('category')
        validated_data.update({'category': c})
        product = Product.objects.create(**validated_data)
        return product

class ItemDetailsSerializer(serializers.ModelSerializer):

    class Meta():
        model = ItemDetails
        fields = ['product', 'quantity']
    

class CartSerializer(serializers.ModelSerializer):
    item = ItemDetailsSerializer()
    class Meta:
        model = Cart
        fields = ['item', 'store_link']
    def create(self, validated_data):
        print(validated_data['item'])
        print("===")
        print(self.data)
        print("===")
        print(validated_data['item'])
        items = validated_data['item']
        for item in items:
            print(validated_data['item'])
        #c, _ = Cart.objects.get_or_create(name=validated_data['item'])
        #validated_data.pop('category')
        #validated_data.update({'category': c})
        #product = Product.objects.create(**validated_data)
        return "product"


class CustomerSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=5, read_only=True)
    phone_number = serializers.CharField(source='username')
    class Meta():
        model = Customer
        fields = ['otp', 'phone_number', 'address']

    def validate(self, attrs):
        attrs.update({'password': ''})
        return attrs


