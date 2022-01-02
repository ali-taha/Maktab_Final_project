from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import RegisterSeller , SelllerLoginForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse
from django.contrib import messages
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

class SignInSeller(FormView):
    template_name = "shop_dashboard/sign-in.html"
    form_class = SelllerLoginForm

    def form_valid(self, form):
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None:
                login(self.request, user)
                messages.success(self.request, "You have logged in successfully")
            else:
                HttpResponse("user not true")  
            return super().form_valid(form)  

    def get_success_url(self):
        return reverse('dashboard')


class SignUpSeller(FormView):
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
            messages.success(self.request, "You have successfully joined")
            return super().form_valid(form)  

    def get_success_url(self):
        return reverse('dashboard')

class TemplateView4(TemplateView):
    template_name = "shop_dashboard/profile.html" 

class TemplateView5(TemplateView):
    template_name = "shop_dashboard/tables.html"         

