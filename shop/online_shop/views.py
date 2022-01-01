from django.shortcuts import render
from django.views.generic import TemplateView

class TemplateView(TemplateView):
    template_name = "shop_dashboard/index.html"

class TemplateView2(TemplateView):
    template_name = "shop_dashboard/sign-in.html"


class TemplateView3(TemplateView):
    template_name = "shop_dashboard/sign-up.html"    

class TemplateView4(TemplateView):
    template_name = "shop_dashboard/profile.html" 

class TemplateView5(TemplateView):
    template_name = "shop_dashboard/tables.html"         

