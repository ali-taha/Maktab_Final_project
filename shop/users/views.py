import redis
from django.views.generic.edit import FormView
from django.views.generic import View
from .forms import RegisterSeller, SelllerLoginForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import (
    redirect,
    render,
    get_list_or_404,
    get_object_or_404,
    HttpResponse,
)
from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
import random
import json, requests
from django.db.models import Q, Avg, Count, Sum
from rest_framework.parsers import FormParser, MultiPartParser


User = get_user_model()
redis_client = redis.StrictRedis(decode_responses=True)


class SignUpSeller(FormView):
    template_name = "login/sign-up.html"
    form_class = RegisterSeller

    def form_valid(self, form):
        user = User.objects.create_user(
            form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            phone_number=form.cleaned_data["phone_number"],
            is_seller=True,
        )
        user.save()
        messages.success(self.request, "You have successfully joined")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("sign_in")


class SignInSeller(FormView):
    template_name = "login/sign-in.html"
    form_class = SelllerLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('store_list'))
        """Handle GET requests: instantiate a blank version of the form."""
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
        )
        if user is not None and user.is_seller:
            login(self.request, user)
            messages.success(self.request, "You have logged in successfully")
        else:
            return HttpResponse("User is not valid")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "store_list",
        )
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("sign_in"))


