"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from users.views import SignUpSeller, SignInSeller, LogoutView, SignUpApi, ProfileApi
from online_shop.views import StoreListApi
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('',SignInSeller.as_view(), name='sign_in'),
    path('sign-up',SignUpSeller.as_view() , name='sign_up'),
    path('logout',LogoutView.as_view() , name='logout_view'),
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls')),
    path('dashboard/',include('online_shop.urls')),

    path('api/sign-up',SignUpApi.as_view(), name='sign_up_api'),
    path('api/sign-in/', TokenObtainPairView.as_view(), name='sign_in_api'),
    path('api/sign-in/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/<username>',ProfileApi.as_view(), name='profile_api'),
    
    path('api/shop/list',StoreListApi.as_view(), name='store_list_api'),


    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Shop Admin'
