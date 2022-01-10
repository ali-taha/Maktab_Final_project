from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView, View
from django.views.generic.edit import FormView, ModelFormMixin, FormMixin
from .forms import CreateStoreForm, AddProductForm, UpdateBasketForm
from django.contrib.auth import  get_user_model
from django.urls import reverse
from django.contrib import messages
from .models import Store, Product, Basket, BasketItem, StoreType
from django.http import Http404
from django.db.models.functions import TruncMonth
from django.db.models import Q, Avg, Count, Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404, HttpResponse
from .filter import BasketListFilter
from django.db.models import OuterRef, Subquery
from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import StoreListSerializer, StoreTypeListSerializer, ProductListSerializer
from .filter import StoreListFilter, StoreTypeFilter,ProductListFilter


User = get_user_model()


class SellerStoreList(ListView):
    template_name = 'seller_dashboard/store_list.html'
    paginate_by = 100

    def get_queryset(self, *args, **kwargs):
        queryset = Store.alive.filter(owner=self.request.user)
        return queryset        

class CreateStore(FormView):
      login_required = True
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


class SellerProductList(ListView):
    template_name = 'seller_dashboard/product_list.html'
    paginate_by = 100

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(store__owner=self.request.user)
        return queryset        


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


class EditProduct(UpdateView):
    template_name = 'seller_dashboard/edit_product.html'  
    model = Product

    fields = ["store", "category", "title", "tag","stock", "image", "description", "price"]

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(UpdateView, self).get_object()
        if not obj.store.owner == self.request.user:
            raise Http404
        return obj         

    def get_success_url(self):
        return reverse('product_list')   


class DeleteProduct(DeleteView):
    template_name = 'seller_dashboard/delete_product.html' 
    model = Product

    def get_success_url(self):
        return reverse('product_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DeleteView, self).get_object()
        if not obj.store.owner == self.request.user:
            raise Http404
        return obj       

    
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
        context["store"] = Store.objects.get(id=self.kwargs['pk'])
        context["filter"] = BasketListFilter(self.request.GET, queryset=self.get_queryset())
        return  context


class BasketDetail(ListView):
    template_name = 'seller_dashboard/basket_detail.html'
    
    def get_queryset(self, *args, **kwargs):
        queryset = BasketItem.objects.filter(basket__id=self.kwargs['pk'])
        return queryset

    def get_context_data(self,*args, **kwargs):
        context = super(BasketDetail, self).get_context_data(*args,**kwargs)
        context['basket'] = Basket.objects.get(id=self.kwargs['pk'])
        return context  


class UpdateBasketStatus(UpdateView):
    model = Basket
    form_class = UpdateBasketForm

    def get_success_url(self):
        return HttpResponse(status=200) 


class SellerProfile(DetailView):
    template_name = 'seller_dashboard/profile.html'
    model = User    
                         
class BuyersList(ListView):
    template_name = 'seller_dashboard/buyers_list.html'
  

    def get_queryset(self, *args, **kwargs):
        latest_buy = Subquery(Basket.objects.filter(owner_id=OuterRef("owner")).order_by("updated_on").values('updated_on')[:1])
        queryset = Basket.objects.filter(Q(store__owner=self.request.user)&Q(status='pai')).values('owner__username').order_by('owner').annotate(totalb=Count('owner')).annotate(totalp=Sum('total_price')).annotate(totali=Sum('count_items')).annotate(lastbuy=latest_buy)
        return queryset      

class ChartView(View):

    def get(self, request, *args, **kwargs):
        store_id = self.kwargs['pk']
        sells = Basket.objects.filter(Q(store_id=store_id)&Q(status="pai")).annotate(month=TruncMonth('paid_on')).values('month').annotate(order_count=Count('id')).values('month', 'order_count')     
        months=[]
        month_sell=[]
        for item in sells:
                months.append(item['month'].strftime('%B'))
                month_sell.append(item['order_count'])
        return render(request, "seller_dashboard/chart.html",{"months":months,"order_count":month_sell})



    """                API  Views                        """


class StoreListApi(generics.ListAPIView):
    filterset_class = StoreListFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreListSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Store.alive.filter(status='con')


class StoreTypeListApi(generics.ListAPIView):
    filterset_class = StoreTypeFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreTypeListSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return StoreType.objects.all()    


class ProductListApi(generics.ListAPIView):
    filterset_class = ProductListFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductListSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Product.available.filter(store__id=self.kwargs.get('store'))                    





