from django.contrib import admin
from .models import CustomUser
from django.utils.html import format_html


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','phone_number','is_seller','is_staff','date_joined')
    list_filter = ('is_staff','is_seller','date_joined')
    search_fields = ('username','first_name','phone_number')
    list_editable = ('is_seller',)
    empty_value_display = '-empty-'

    @admin.display(empty_value='EMPTY', description='image')
    def view_avater(self, obj):
         return format_html(
            '<image src="{}" width=70 height=70>',
            obj.user_avater.url,
        )

admin.site.register(CustomUser,CustomUserAdmin)