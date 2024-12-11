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
from .views import (home , user_login , logout_view ,
                    creat_receiver, register_view ,
                    user_list ,delete_user ,update_user ,
                    reciever_list ,delete_receiver , edit_receiver ,import_reciever,
                    errolog_list
                    )
urlpatterns = [
    path('' , home , name='home') ,
    path ('login/' , user_login , name ='login') ,
    path ('import_reciever/' , import_reciever , name ='import_reciever') ,
    path('logout/' , logout_view , name ='logout' ) ,
    path('create-user' ,  register_view ,name= 'creat-user') ,
    path('user_list' ,  user_list ,name= 'user_list'),
    path('delete_user/<id>' ,  delete_user ,name= 'delete_user') ,
    path('update_user/<id>' ,  update_user ,name= 'update_user') ,
    path('reciever_list' ,  reciever_list ,name= 'reciever_list') ,
    path('creat_receiver' ,  creat_receiver ,name= 'creat_receiver') ,
    path('delete_receiver/<id>' ,  delete_receiver ,name= 'delete_receiver') ,
    path('edit_receiver/<id>' ,  edit_receiver ,name= 'edit_receiver') ,
    path ('errolog_list/' , errolog_list , name ='errolog_list') ,

]
