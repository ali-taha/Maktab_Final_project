from django.contrib import admin
from .models import ProductCategory, ProductTag, StoreType, Store, Product, Basket, BasketItem
from django.utils.html import format_html


@admin.action(description='Mark store as Confirmed')
def make_confirmed(modeladmin, request, queryset):
    queryset.update(status='con')

@admin.action(description='Mark store as Deleted')
def make_deleted(modeladmin, request, queryset):
    queryset.update(status='del')    

@admin.action(description='Mark store as Review')
def make_review(modeladmin, request, queryset):
    queryset.update(status='rev')  

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','status','created_on','type',)
    list_filter = ('status','created_on','type')
    search_fields = ('title',)
    date_hierarchy = 'created_on'
    list_editable = ('status',)
    actions = [make_confirmed, make_deleted, make_review]
    empty_value_display = '-empty-'
    

admin.site.register(Store,StoreAdmin) 


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','store','get_owner','stock','price', 'view_image','category')
    list_filter = (('category__title', custom_titled_filter('Category')),)
    search_fields = ('title',)
    empty_value_display = '-empty-'

    def get_owner(self, obj):
        return obj.store.owner
    get_owner.short_description = 'Owner'
    get_owner.admin_order_field = 'store__owner'

    @admin.display(empty_value='EMPTY', description='image')
    def view_image(self, obj):
         return format_html(
            '<image src="{}" width=70 height=70>',
            obj.image.url,
        )

admin.site.register(Product, ProductAdmin)



class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'total_price','count_items', 'status', 'store')
    list_editable = ('status',)
    list_filter = ('status','paid_on','store')
    search_fields = ('store','owner')

admin.site.register(Basket,BasketAdmin)


class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'id', 'product', 'count','buy_price')
    search_fields = ('basket','product')

admin.site.register(BasketItem,BasketItemAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    search_fields = ('title','parent')
    list_filter = ('title','parent')

admin.site.register(ProductCategory,ProductCategoryAdmin)

class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)

admin.site.register(ProductTag,ProductTagAdmin)


class StoreTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)

admin.site.register(StoreType,StoreTypeAdmin)
