from django.urls import path
from users.views import SignUpSeller, SignInSeller, LogoutView


urlpatterns = [

    path('',SignInSeller.as_view(), name='sign_in'),
    path('sign-up',SignUpSeller.as_view() , name='sign_up'),
    path('logout',LogoutView.as_view() , name='logout_view'),

]