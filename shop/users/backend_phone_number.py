from django.contrib.auth.backends import ModelBackend 
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from django.db.models import Q
from rest_framework.exceptions import APIException


User = get_user_model()

class UserOrPassNotCorrect(APIException):
    status_code = 401
    default_detail = 'Username or Password is Not Correct'
    default_code = 'userpass_unavailable'


class CustomAuthentication(ModelBackend):

    def authenticate(self, request, username, password, **kwargs):
        # phone_number = username
        try:
            user = User.objects.get(Q(phone_number=username)&Q(is_seller=False))
            if user.check_password(password) is True:
                return user
            else:
                raise UserOrPassNotCorrect
        except User.DoesNotExist:
            pass