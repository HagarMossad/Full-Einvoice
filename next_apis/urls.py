from django.urls import path
from .views import  recive_invoice_data

urlpatterns = [
    path('recive_invoice_data' ,recive_invoice_data , name='recive_invoice_data' ),

]