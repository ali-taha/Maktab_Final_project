from django.views.generic.edit import FormView
from django.views.generic import View
from .forms import RegisterSeller , SelllerLoginForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404, HttpResponse


User = get_user_model()


class SignUpSeller(FormView):
    template_name = "login/sign-up.html" 
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
        return reverse('sign_in')


class SignInSeller(FormView):
    template_name = "login/sign-in.html"
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
        id = self.request.user.id
        return reverse('dashboard',)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('sign_in'))        