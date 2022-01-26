from django.urls import path
from users.api.views import SignUpApi, ProfileApi, ConfirmPhoneNumber, RequestCodeForLogin, RequestActiveCode
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
# from users.customer_token import MyTokenObtainPairView


urlpatterns = [
    path('sign-up',SignUpApi.as_view(), name='sign_up_api'),
    path('sign-in/', TokenObtainPairView.as_view(), name='sign_in_api'),
    # path('sign-in/', MyTokenObtainPairView.as_view(), name='sign_in_api'),
    path('sign-in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<username>',ProfileApi.as_view(), name='profile_api'),
    
    path('request-active-code/',RequestActiveCode.as_view() , name='request_code'),
    path('confirm-number/',ConfirmPhoneNumber.as_view() , name='confirm_number'),
    path('request-login-code/', RequestCodeForLogin.as_view(), name='request_login_code_api'),
]
