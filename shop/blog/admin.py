from django.contrib import admin
from .models import BlogCategory, Post, BlogComment, BlogTag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','writer','created_at','is_published','like')
    list_filter = ('is_published','created_at')
    search_fields = ('title','description')
    date_hierarchy = 'created_at'
    list_editable = ('is_published',)
    empty_value_display = '-empty-'

admin.site.register(Post,PostAdmin)


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    search_fields = ('title','parent')
    list_filter = ('title','parent')

admin.site.register(BlogCategory,BlogCategoryAdmin)


class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)
    list_filter = ('title',)

admin.site.register(BlogTag,BlogTagAdmin)


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('title','user','post','createed_at' )
    search_fields = ('title','user','post')
    list_filter = ('title','createed_at')

admin.site.register(BlogComment,BlogCommentAdmin)