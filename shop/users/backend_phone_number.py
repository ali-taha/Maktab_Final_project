from django.contrib.auth.backends import ModelBackend 
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.db.models import Q

User = get_user_model()


class CustomAuthentication(ModelBackend):

    def authenticate(self, request, username, password, **kwargs):
        # phone_number = username
        try:
            user = User.objects.get(Q(phone_number=username)&Q(is_seller=False))
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass