from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.views.generic.edit import FormView
from .forms import RegisterSeller , SelllerLoginForm, CreateStoreForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.urls import reverse
from django.contrib import messages
from .models import Store
from django.http import Http404
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
 


class CreateStore(FormView):
      template_name = "shop_dashboard/create_store.html"  
      form_class = CreateStoreForm 


      def form_valid(self, form):
            store = Store.objects.create(
            title = form.cleaned_data["title"],
            description =form.cleaned_data["description"],
            type=form.cleaned_data["type"],
            location_lat=form.cleaned_data["location_lat"],
            location_lng=form.cleaned_data["location_lng"],
            owner = self.request.user,
        )
            store.save()
            messages.success(self.request, "Your store successfully Created, Wait for Confirm")
            return super().form_valid(form)  

      def get_success_url(self):
        return reverse('store_detail') 


class SellerStoreList(ListView):
    template_name = 'shop_dashboard/store_list.html'
    paginate_by = 100

    def get_queryset(self, *args, **kwargs):
        queryset = Store.alive.filter(owner=self.request.user)
        return queryset

class DeleteStore(DeleteView):
    template_name = 'shop_dashboard/delete_store.html' 
    model = Store

    def get_success_url(self):
        return reverse('store_detail')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj       
     
                  

