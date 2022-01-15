from django.contrib.auth.backends import ModelBackend 
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.db.models import Q

User = get_user_model()


class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request, **kwargs):
        try:
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')
            user = User.objects.get(Q(phone_number=phone_number)&Q(is_seller=False))
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass