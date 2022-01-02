from django.urls import path
from .views import *


urlpatterns = [
    path('',TemplateView.as_view(), name='dashboard'),
    path('sign-in',TemplateView2.as_view(), name='sign-in'),
    path('sign-up',TemplateView3.as_view() , name='sign-up'),
    path('profile',TemplateView4.as_view(), name= 'profile'),
    path('tables',TemplateView5.as_view()),
]