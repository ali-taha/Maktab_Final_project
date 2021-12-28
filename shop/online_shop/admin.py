from django.contrib import admin
from .models import ProductCategory, ProductTag, StoreType, Store, Product, Basket, BasketItem
from django.utils.html import format_html

admin.site.register(ProductCategory)
admin.site.register(ProductTag)
admin.site.register(StoreType)
admin.site.register(Basket)
admin.site.register(BasketItem)


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
    list_display = ('title','owner','status','created_on','type')
    list_filter = ('status','created_on','type')
    search_fields = ('title',)
    date_hierarchy = 'created_on'
    list_editable = ('status',)
    actions = [make_confirmed, make_deleted, make_review]

admin.site.register(Store,StoreAdmin) 


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_image',)

    @admin.display(empty_value='EMPTY', description='image')
    def view_image(self, obj):
         return format_html(
            '<image src="{}" width=70 height=70>',
            obj.image.url,
        )

admin.site.register(Product, ProductAdmin)
