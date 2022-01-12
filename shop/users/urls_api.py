from django.urls import path
from users.views import SignUpSeller, SignInSeller, LogoutView, SignUpApi, ProfileApi
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)



urlpatterns = [
    path('sign-up',SignUpApi.as_view(), name='sign_up_api'),
    path('sign-in/', TokenObtainPairView.as_view(), name='sign_in_api'),
    path('sign-in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<username>',ProfileApi.as_view(), name='profile_api'),
]
