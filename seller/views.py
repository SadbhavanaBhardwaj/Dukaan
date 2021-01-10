from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
import json
# Create your views here.
from .models import Owner, Store
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .serializers import OwnerSerializer, StoreSerializer
from buyer.serializers import ProductSerializer
from rest_framework.generics import CreateAPIView


class OwnerSignUpAPIView(APIView):
    def post(self, request):
        data = request.data
        user = request.user
        serializer = OwnerSerializer(data=data)      
        if serializer.is_valid():
            print("valie")
            serializer.save()
        else:
            print(serializer.errors)
        #print(serializer.data['phone_number'])
        owner = Owner.objects.get(username=serializer.data['phone_number'])
        #print(owner.id)
        token, created=Token.objects.get_or_create(user=owner)
        data={"phone": owner.username, "token": token.key}
        return HttpResponse(json.dumps(data),content_type='application/json')



class StoreView(APIView):
    authentication_classes = (TokenAuthentication, )
    
    def post(self, request):
        print(request.META['HTTP_AUTHORIZATION'])
        user = Token.objects.get(key=request.META['HTTP_AUTHORIZATION'].split(' ')[1]).user
        data = request.data
        user = Owner.objects.get(username=user.username)
        data.update({"owner": user})
        
        print(data['address'])
        store = Store.objects.create(store_name=data['store_name'], address=data['address'], owner=data['owner'])
        #serializer = StoreSerializer(data=data)
        path = request.get_full_path()+request.META['HTTP_HOST']+"/"    
        data = {"store_id": store.id, "store-link": path+store.slug+"/"}
        return HttpResponse(json.dumps(data),content_type='application/json')


class ProductAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    def post(self, request):
        data = request.data
        print(data)
        serializer = ProductSerializer(data=data)      
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        data = {"id": serializer.data['id'], 'name': serializer.data['product_name'], "image": serializer.data['image']}
        return HttpResponse(json.dumps(data), content_type='application/json')
