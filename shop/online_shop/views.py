from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView, View
from django.views.generic.edit import FormView, ModelFormMixin, FormMixin
from .forms import CreateStoreForm, AddProductForm, UpdateBasketForm
from django.contrib.auth import  get_user_model
from django.urls import reverse
from django.contrib import messages
from .models import Store, Product, Basket, BasketItem
from django.http import Http404
from django.db.models.functions import TruncMonth
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404, HttpResponse
from .filter import BasketListFilter



User = get_user_model()



class SellerStoreList(ListView):
    template_name = 'seller_dashboard/store_list.html'
    paginate_by = 100

    def get_queryset(self, *args, **kwargs):
        queryset = Store.alive.filter(owner=self.request.user)
        return queryset        


class CreateStore(FormView):
      template_name = "seller_dashboard/create_store.html"  
      form_class = CreateStoreForm 

      def form_valid(self, form):
            denied = Store.objects.filter(Q(owner=self.request.user) & Q(status ='rev'))
            if not denied:
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
            else:
                messages.warning(self.request, "You Have a Store in Review Mode")  
                return super().form_invalid(form)   

      def get_success_url(self):
        return reverse('store_list') 


class EditStore(UpdateView):
    template_name = 'seller_dashboard/edit_store.html'  
    model = Store

    fields = ["title", "description", "type", "location_lat","location_lng"]

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(UpdateView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj         

    def get_success_url(self):
        return reverse('store_list')   

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'rev'
        self.object.save()
        return super().post(request, *args, **kwargs)          


class DeleteStore(DeleteView):
    template_name = 'seller_dashboard/delete_store.html' 
    model = Store

    def get_success_url(self):
        return reverse('store_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj   


class AddProduct(FormView):
    template_name = "seller_dashboard/add_product.html"        
    form_class = AddProductForm

    def get_form_kwargs(self):
        kwargs = super(AddProduct, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your Product successfully Added")
        return super().form_valid(form)    

    def get_success_url(self):
        return reverse('store_list')     

    
class StoreBasketList(FormMixin,ListView):
    template_name = 'seller_dashboard/basket_list.html'
    paginate_by = 100
    form_class = UpdateBasketForm

    def get_queryset(self):
            store = Store.objects.get(id=self.kwargs['pk'])
            queryset = Basket.objects.filter(store = store)
            return queryset   

    def get_context_data(self, **kwargs):
        context = super(StoreBasketList, self).get_context_data(**kwargs)
        # context["form"] = self.get_form()
        context["pk"] = self.kwargs['pk']
        context["filter"] = BasketListFilter(self.request.GET, queryset=self.get_queryset())
        return  context

    # def get_context_data(self,*args, **kwargs):
    #     context = super(StoreBasketList, self).get_context_data(*args,**kwargs)
    #     context['store'] = Store.objects.get(id=self.kwargs['pk'])
    #     return context    

    # def get_queryset(self, *args, **kwargs):
    #     store = Store.objects.get(id=self.kwargs['pk'])
    #     queryset = Basket.objects.filter(store = store)
    #     return queryset

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         id=self.kwargs['pk'] 
    #         status = form.cleaned_data['status']
    #         obj = Basket.objects.get(id=id)
    #         obj.status = status
    #         obj.save()
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

class BasketDetail(ListView):
    template_name = 'seller_dashboard/basket_detail.html'
    
    def get_queryset(self, *args, **kwargs):
        queryset = BasketItem.objects.filter(basket__id=self.kwargs['pk'])
        return queryset

    def get_context_data(self,*args, **kwargs):
        context = super(BasketDetail, self).get_context_data(*args,**kwargs)
        context['basket'] = Basket.objects.get(id=self.kwargs['pk'])
        return context  

class UpdateMyStatus(UpdateView):
    model = Basket
    form_class = UpdateBasketForm

    def get_success_url(self):
        return reverse('store_list')                  
        
    
class ChartView(View):

    def get(self, request, *args, **kwargs):
        store_id = self.kwargs['pk']
        sells = Basket.objects.filter(Q(store_id=store_id)&Q(status="pai")).annotate(month=TruncMonth('paid_on')).values('month').annotate(order_count=Count('id')).values('month', 'order_count')                    
        month=[]
        month_sell=[]
        for item in sells:
                month.append(item['month'].strftime('%B'))
                month_sell.append(item['order_count'])
        return render(request, "seller_dashboard/chart.html",{"months":month,"order_count":month_sell})

    

         
            

class TemplateView4(TemplateView):
    template_name = "seller_dashboard/profile.html" 

class TemplateView(TemplateView):
    template_name = "shop/main_shop_dashboard.html"