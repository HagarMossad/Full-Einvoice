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

from django.urls import path
from .views import *

urlpatterns = [
    path('taxes_list' , taxes_list , name='taxes_list') ,
    path('taxestype_list' , taxestype_list , name='taxestype_list') ,
    path('taxessubtype_list' , taxessubtype_list , name='taxessubtype_list') ,
    path('get_available_subtype' , get_available_subtype , name='get_available_subtype') ,
    path('creat_tax' , creat_tax , name='creat_tax') ,
    path('tax_details/<id>' , tax_details , name='tax_details') ,
    path('delete_tax/<id>' , delete_tax , name='delete_tax') ,
    path('delete_taxable_item/<id>' , delete_taxable_item , name='delete_taxable_item') ,
 

]
