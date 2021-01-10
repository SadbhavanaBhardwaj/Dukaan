from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
import json
from .serializers import CartSerializer, CustomerSerializer
from .models import Store, Product, Order, Cart, Customer, ItemDetail
# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView

from django.db.models.query import QuerySet

class StoreDetailsAPIView(APIView):
    def post(self, request):
        data = request.data
        store_link = data['store_link']
        slug = store_link.split('/')[5]
        print(slug)
        store = Store.objects.get(slug=slug)
        data = {"store_id": store.id, "store name": store.store_name, "address": store.address}
        return HttpResponse(json.dumps(data), content_type='application/json')

#{"store_link": "http://127.0.0.1:8000/seller/store/store-1-3445/"}

class ProductDetails(APIView):
    def post(self, request):
        data = request.data
        store_link = data['store_link']
        slug = store_link.split('/')[5]
        store = Store.objects.get(slug=slug)
        list_cat = list(Product.objects.filter(store=store).values_list('category', flat=True))
        query = Product.objects.filter(store=store).query
        query.group_by = ['category']
        products = QuerySet(query=query, model=Product)
        for cats in list_cat:
            pass
        print(products)
        return HttpResponse(products)


class CartItemsAPIView(APIView):
    """
        if pk of cart isnot  provided in the body, then a new cart is created,
        otherwise items are added to that cart
        for a given cart, if the product is already present then only the quantity is change 
        otherwise the product is added to the cart or removed from the cart
    """
    serializer_class = CartSerializer
    def post(self, request):
        data = request.data
        print(data)
        if 'pk' in request.data:
            cart = Cart.objects.get(id=data['pk'])
        else:
            cart = Cart.objects.create(store_link=data['store_link']) 
        product_id = data['product_id']
        quantity = data['quantity']
        product = Product.objects.get(id=product_id)
        if ItemDetail.objects.filter(product=product, cart=cart):
            item = ItemDetail.objects.get(product=product, cart=cart)
            item.quantity = quantity
            item.save()
            if quantity == 0:
                item.delete()
        else:
            item = ItemDetail.objects.create(product=product, quantity=quantity, cart=cart)
        return HttpResponse(json.dumps({"data": "cart has been updated"}), content_type='application/json')


class OrderAPIView(APIView):
    def post(self, request, pk):
        if 'HTTP_AUTHORIZATION' in request.META['HTTP_AUTHORIZATION']:
            user = Token.objects.get(key=request.META['HTTP_AUTHORIZATION'].split(' ')[1]).user
            user = Customer.objects.get(username=user.username)
        elif 'phone_number' in request.data:
            data = request.data
            user = request.user
            serializer = CustomerSerializer(data=data)      
            if serializer.is_valid():
                print("valid")
                serializer.save()
            else:
                print(serializer.errors)
            #print(serializer.data['phone_number'])
            user = Customer.objects.get(username=serializer.data['phone_number'])
            #print(owner.id)
            token, created=Token.objects.get_or_create(user=user)
        else:
            return HttpResponse({"data": "Kindly provide phone number or authorize using token"})
        order = Order.objects.create(cart=Cart.objects.get(pk=pk), customer=user)
        data = {"order_id": order.id}
        return HttpResponse(json.dumps(data), content_type='application/json')
