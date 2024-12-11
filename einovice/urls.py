"""einovice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include , include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('home.urls')) ,
    path('payer/ ', include('payer.urls')) ,
     path('taxes/ ', include('tax.urls')) ,
     path('main/' , include('invoice.urls')) ,
     path('reports/' , include('reports.urls')),
    
     path('ereciept/', include('ereciept.urls')),
     path('api/', include('next_apis.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
