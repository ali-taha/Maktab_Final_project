from django.contrib.auth.backends import ModelBackend 
from django.contrib.auth import get_user_model
from django.db.models import Q
import redis
from rest_framework.exceptions import APIException

User = get_user_model()
redis_client = redis.StrictRedis(decode_responses=True)

def check_otp_code(user,otp_code):
        redis_otp = redis_client.get(f'otp:{user.phone_number}')
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
        # phone_number = username
        try:
            user = User.objects.get(Q(phone_number=username)&Q(is_seller=False))
            if  check_otp_code(user,password) is True:
                return user 
            else:
                raise CodeUnavailable     
        except User.DoesNotExist:
            pass
            
