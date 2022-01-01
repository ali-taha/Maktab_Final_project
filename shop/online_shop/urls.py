from django.urls import path
from .views import *

urlpatterns = [
    path('',TemplateView.as_view()),
    path('sign-in',TemplateView2.as_view()),
    path('sign-up',TemplateView3.as_view()),
    path('profile',TemplateView4.as_view()),
    path('tables',TemplateView5.as_view()),
]