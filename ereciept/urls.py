from django.urls import path, include

from ereciept.views import get_invoice_json 
from .rviews.home import home
from .rviews.uplaod_file import upload_file ,craete_reciept_api
from .rviews.reciept import (new_reciept ,create_invocie_json_return,
                            get_reciept ,add_receiept_item ,add_receiept_item ,edit_receiept_item,
                            post_receipt_data ,create_invocie_json ,delete_reciept_line ,reciept_line_details)
from  .rviews.tax_view import tax_list ,creat_tax, tax_details
from .rviews.seller import *  
from .views import init_tax_types,init_tax_sup_types , tax_sub_type_list, tax_type_list
urlpatterns = [
    path('', home, name="home-list"), 
    path('seller', seller_list , name="seller-list"), 
    path('reciept_tax',tax_list, name="reciept_tax"),
    path('reciept_creat_tax',creat_tax, name="reciept_creat_tax"),
    path('reciept_tax_details/<id>',tax_details , name="reciept_tax_details"),
    path('create_invocie_json/<pk>',create_invocie_json , name="create_invocie_json"),
    path('reciept_line_details/<pk>',reciept_line_details , name="reciept_line_details"),
    path('create_invocie_json_return/<pk>',create_invocie_json_return, name="create_invocie_json_return"),
    path('new_reciept', new_reciept, name="new_reciept"),
    path('upload_file', upload_file, name="upload_file"),
    path('add_receiept_item', add_receiept_item, name="add_receiept_item"),
    path('edit_receiept_item', edit_receiept_item, name="edit_receiept_item"),
    path('post_receipt_data', post_receipt_data, name="post_receipt_data"),
    path('craete_reciept_api', craete_reciept_api, name="craete_reciept_api"),
    path('delete_reciept_line',delete_reciept_line, name="delete_reciept_line"),
    path('get_reciept/<pk>',get_reciept , name="get_reciept"),
    path('get_invoice_json', get_invoice_json),
    path('init_tax_types', init_tax_types ,name = "e_init_tax_types"),
    path('init_tax_sup_types', init_tax_sup_types ,name = "e_init_tax_sup_types"),
    path('tax_type_list', tax_type_list ,name="e_tax_type_list"),
    path('tax_sub_type_list', tax_sub_type_list , name ="e_tax_sub_type_list"),
   
]
