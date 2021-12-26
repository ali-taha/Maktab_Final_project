from django.contrib import admin

from .models import BlogCategory, Post, BlogComment, BlogTag

admin.site.register(BlogCategory)
admin.site.register(Post)
admin.site.register(BlogComment)
admin.site.register(BlogTag)