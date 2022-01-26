from django.contrib.auth.backends import ModelBackend 
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import APIException
from django.core.cache import cache

User = get_user_model()

def check_otp_code(phone_number,otp_code):
        redis_otp = str(cache.get(f'login_code:{phone_number}'))
        if redis_otp == otp_code:
            return True
        else:
            return False 

class CodeUnavailable(APIException):
    status_code = 401
    default_detail = 'Code is Not Available'
    default_code = 'code_unavailable' 
            
class CustomAuthenticationOtp(ModelBackend):

    def authenticate(self, request, username, password, **kwargs):
        phone_number = username
        try:
            user = User.objects.get(Q(phone_number=phone_number)&Q(is_seller=False))
            if  check_otp_code(phone_number,password) is True:
                return user 
            else:
                raise CodeUnavailable     
        except User.DoesNotExist:
            pass
            
