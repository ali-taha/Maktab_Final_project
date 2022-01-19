from django.urls import path
from users.views import SignUpApi, ProfileApi, OtpPhoneNumber, RequestOtpCode, LoginWithCode
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
# from users.customer_token import MyTokenObtainPairView



urlpatterns = [
    path('sign-up',SignUpApi.as_view(), name='sign_up_api'),
    path('sign-in/', TokenObtainPairView.as_view(), name='sign_in_api'),
    # path('sign-in/', MyTokenObtainPairView.as_view(), name='sign_in_api'),
    path('sign-in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<username>',ProfileApi.as_view(), name='profile_api'),
    
    path('otp/',OtpPhoneNumber.as_view() , name='otp_view'),
    path('request-otp/', RequestOtpCode.as_view(), name='request-otp-api'),
    path('login-with-code/', LoginWithCode.as_view(), name='login-with-code-api'),


]
