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
from .views import invoice_list ,upload_page,create_inoice ,edit_invocie ,uplaod_sheet ,post_to_auth,export_to_excel
urlpatterns = [
    path('invoice_list' ,invoice_list , name='invoice_list' ),
    path('create_inoice' ,create_inoice , name='create_inoice' ),
     path('edit_invocie/<id>' ,edit_invocie , name='edit_invocie' ),
     path('upload' ,uplaod_sheet, name='upload'),
     path('upload_page/<id>' ,upload_page, name='upload_page'),
     path('post_to_auth/<id> ' ,post_to_auth, name='post_to_auth'),
     path('export_to_excel',export_to_excel,name='export_to_excel')
]