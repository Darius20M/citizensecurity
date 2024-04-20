"""
URL configuration for citizensecurity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    re_path('schema/', SpectacularAPIView.as_view(), name='schema'),
    re_path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    re_path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    re_path('^admin/', admin.site.urls),
    re_path('^security/', include('security.urls')),
    re_path('^auth/', include('security.auth_urls')),
    re_path('^auth/registration/', include('security.registration_urls'))

]
