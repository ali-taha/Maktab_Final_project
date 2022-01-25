import redis
from django.views.generic.edit import FormView
from django.views.generic import View
from users.forms import RegisterSeller, SelllerLoginForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import (
    redirect,
    render,
    get_list_or_404,
    get_object_or_404,
    HttpResponse,
)
from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
from users.api.serializers import UserSignUpSerializer, UserDetailSerializer, UserUpdateSerializer, OtpRequestSerializer,RequestOtpCodeSerializer
import random
import json, requests
from django.db.models import Q, Avg, Count, Sum
from rest_framework.parsers import FormParser, MultiPartParser


User = get_user_model()
redis_client = redis.StrictRedis(decode_responses=True)



class SignUpApi(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data={"msg": "User successfully created"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
        
class ProfileApi(generics.RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    lookup_field = "username"
    lookup_field_kwargs ="username"
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
            return User.objects.filter(id=self.request.user.id) 

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserDetailSerializer
        elif self.request.method == "PUT":
            return UserUpdateSerializer 
        elif self.request.method == "PATCH":
            return UserUpdateSerializer 

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.data.get('phone_number'):
            new_phone = self.request.data.get('phone_number')
            old_phone = self.request.user.phone_number
            if new_phone != old_phone:
                serializer.save(is_phone_active=False)
        serializer.save()    

def get_otpcode(phone_number, type):
        otp = random.randint(1000,9999)
        if type == 'activation':
            redis_client.set(f'active_code:{phone_number}',otp, ex=300)
        elif type == 'logincode':
            redis_client.set(f'login_code:{phone_number}',otp, ex=300)

        url = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
        payload = json.dumps({
        "username": "09190771284",
        "password": "6ZRS#",
        "to": f"{phone_number}",
        "from": "50004001771284",
        "text": f"your code : {otp}\n ali_shop"
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return Response(data={"msg":f"code sent to : {phone_number}"}, status=status.HTTP_200_OK) 


class RequestActiveCode(generics.GenericAPIView):
    serializer_class=OtpRequestSerializer

    def post(self, request, *args, **kwargs):
        user_phone = self.request.data.get("phone_number")
        valid_user = User.objects.filter(Q(phone_number=user_phone)&Q(is_phone_active=False)).exists()
        if valid_user:
                return get_otpcode(user_phone, 'activation')   
        else:
            return Response(data={"msg":"phone number is not valid or is activated"}, status=status.HTTP_400_BAD_REQUEST)       
                            
class ConfirmPhoneNumber(generics.GenericAPIView):
    serializer_class = OtpRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = OtpRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)    
        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        saved_code = redis_client.get(f'active_code:{phone}')
        if saved_code: 
            if code == saved_code: 
                    user = User.objects.get(phone_number=phone)
                    user.is_phone_active = True
                    user.save()
                    return Response(data={"msg":f"phone activated : {phone}"}, status=status.HTTP_200_OK) 
            else:
                    return Response(data={"msg":"Code is Not True"}, status=status.HTTP_400_BAD_REQUEST)  
        else:            
            return Response(data={"msg":"Code is Expired"}, status=status.HTTP_400_BAD_REQUEST) 


class RequestCodeForLogin(generics.GenericAPIView):
    serializer_class = RequestOtpCodeSerializer   

    def get_queryset(self):
            phone = self.request.data.get('phone')
            return User.objects.filter(Q(phone_number=phone)&Q(is_phone_active=True)) 
            
    def post(self, request, *args, **kwargs):
        user_phone = self.request.data.get('phone')
        if self.get_queryset():
            return get_otpcode(user_phone, 'logincode')
        else:
            return Response(data={"msg":f"number {user_phone} is not avtive or valid"}, status=status.HTTP_204_NO_CONTENT)              
    



