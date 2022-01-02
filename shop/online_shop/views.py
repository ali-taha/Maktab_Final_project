from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import RegisterSeller
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import (
    redirect,
    render,
    get_list_or_404,
    get_object_or_404,
    HttpResponse,
)



User = get_user_model()


class TemplateView(TemplateView):
    template_name = "shop_dashboard/index.html"

class TemplateView2(TemplateView):
    template_name = "shop_dashboard/sign-in.html"


class TemplateView3(FormView):
    template_name = "shop_dashboard/sign-up.html" 
    form_class = RegisterSeller



    def form_valid(self, form):
            user = User.objects.create_user(
            form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            phone_number=form.cleaned_data["phone_number"],
            is_seller = True,
        )
            user.save()
            return super().form_valid(form)  

    def get_success_url(self):
        return reverse('dashboard')

class TemplateView4(TemplateView):
    template_name = "shop_dashboard/profile.html" 

class TemplateView5(TemplateView):
    template_name = "shop_dashboard/tables.html"         

