from django.db import models

# Create your models here.
from pathlib import Path
import sys
import os 
import json

from payer.models import PayerAccount

BASE_DIR = Path(__file__).resolve().parent.parent
if sys.platform == 'win32' :
    file_path = BASE_DIR  / 'e_invoice\CountryCodes.json'
    tax_path = BASE_DIR / 'e_invoice\TaxTypes.json'
    tax_subtype_path = BASE_DIR / 'e_invoice\TaxSubtypes.json'
    uom_path =  BASE_DIR / r'e_invoice\UnitTypes.json'
else :
    file_path = BASE_DIR  / 'e_invoice/CountryCodes.json'
    tax_path = BASE_DIR / 'e_invoice/TaxTypes.json'
    tax_subtype_path = BASE_DIR / 'e_invoice/TaxSubtypes.json'
    uom_path =  BASE_DIR / r'e_invoice/UnitTypes.json'
countr_json = open(file_path , encoding= 'utf-8')
country_data =json.load(countr_json)
COUNTY_CODES = [(i.get('code') , i.get('Desc_en'))  for i in country_data]




tax_json = open(tax_path ,encoding='utf-8' )
tax_data = json.load(tax_json)
TAXES_CODES = [(i.get('Code') , i.get('Desc_ar') ) for i in tax_data]




tax_subtype_json = open(tax_subtype_path , encoding='utf-8')
tax_subtype_data = json.load(tax_subtype_json)

TAX_SUBTYPE =  [(i.get('Code') , i.get('Desc_ar') ) for i in tax_subtype_data]
# C:\Users\dynamic1\E-invocie\offlinepos\e_invoice\UnitTypes.json

uom_json = open(uom_path  , encoding='utf-8')
uom_data = json.load(uom_json)
UOM =  [(i.get('code') , i.get('desc_en') ) for i in uom_data ]

DOCUMENTTYPE = [('i' , 'Invoice') , 
                ('d' , 'Debit Note' ),
                ('c' ,'Credit Note')]

AccountType=   [('P' , 'Person') ,
                ('B' , 'Business'),
                ('F' , 'Forgien')]



DocumentTypeVersion = [('1.0' , '1.0'),
                       ('0.9' ,'0.9')]



class Receiver(models.Model) :
    payer = models.ForeignKey(PayerAccount , on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField (max_length= 250 , null=True , blank=True)
    receiver_type =models.CharField(max_length=250 , choices= AccountType ,null=True , blank=True)
    receiver_id=models.CharField(max_length=250  , null=True , blank=True)
    receiver_name=models.CharField(max_length=250 , null=True , blank=True)
    receiver_address_branchId=models.CharField(max_length=250 , null=True , blank=True)
    receiver_address_country=models.CharField(max_length=250 ,choices=COUNTY_CODES , default='EG' , null=True , blank=True)
    receiver_address_governate=models.CharField(max_length=250 , null=True , blank=True)
    receiver_address_regionCity=models.CharField(max_length=250 , null=True , blank=True)
    receiver_address_street=models.CharField(max_length=250 , null=True , blank=True)
    receiver_address_buildingNumber=models.CharField(max_length=250 , null=True , blank=True)

class TaxableTypes(models.Model):
    Code     = models.CharField(max_length=250 , null =True , blank=True)
    Desc_en  = models.CharField(max_length=250 , null =True , blank=True)
    Desc_ar  = models.CharField(max_length=250 , null =True , blank=True)

    def __str__(self):
        return self.Desc_en



class TaxSubtypes(models.Model):
    Code              = models.CharField(max_length=250 , null =True , blank=True)
    Desc_en           = models.CharField(max_length=250 , null =True , blank=True)
    Desc_ar           = models.CharField(max_length=250 , null =True , blank=True)
    TaxtypeReference  = models.CharField(max_length=250 , null =True , blank=True)
    def __str__(self):
        return self.Desc_en



class ReceiverFile(models.Model) :
    status = models.CharField(max_length=250 , null=True , blank=True)
    uplaod_time = models.DateTimeField(auto_now_add= True)
    sheet = models.FileField(upload_to = 'uploader')




class ErrorLog(models.Model):
    message = models.TextField(max_length= 1000 , blank=True , null=True)
    refrence = models.CharField(max_length= 250 , null= True , blank=True)
    date = models.DateTimeField(auto_now= True, auto_created=True ,blank=True , null= True)
    nowdate = models.DateTimeField(auto_now= True, auto_created=True ,blank=True , null= True)


    class Meta :
        ordering = ['nowdate']