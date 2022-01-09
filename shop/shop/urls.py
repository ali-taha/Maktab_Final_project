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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users.views import SignUpSeller, SignInSeller, LogoutView, SignUpApi
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)


urlpatterns = [
    path('',SignInSeller.as_view(), name='sign_in'),
    path('sign-up',SignUpSeller.as_view() , name='sign_up'),
    path('logout',LogoutView.as_view() , name='logout_view'),
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls')),
    path('dashboard/',include('online_shop.urls')),

    path('api/sign-up',SignUpApi.as_view(), name='sign_up_api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Shop Admin'
