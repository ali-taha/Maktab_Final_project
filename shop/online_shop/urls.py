from django.urls import path
from .views import *


urlpatterns = [
    path('',TemplateView.as_view(), name='dashboard'),
    path('sign-in',SignInSeller.as_view(), name='sign-in'),
    path('sign-up',SignUpSeller.as_view() , name='sign-up'),
    path('profile',TemplateView4.as_view(), name= 'profile'),
    path('tables',TemplateView5.as_view()),
]