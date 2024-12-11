from datetime import datetime
from django.shortcuts import render , redirect
from ereciept.utils import get_invoice_uuid
from ereciept.models.discountmodel import DiscountObj
from ereciept.models.itemData import itemData
from ereciept.models.taxableItems import taxTotals, taxableItems
from ereciept.models.seller import Seller

from ereciept.models.ereciept import Receiept
from ereciept.serializer import ReceieptSerializer, ReceieptWithoutUUIDSerializer
#/home/beshoy/taxauth/E-recirpt-app/e_inoivce-windows/ereciept.views.py from ereciept.views import init_tax_types, exit()

from .models.TaxTypes import TaxTypes, TaxSubtypes
import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .taxtypes import data

import requests



def tax_type_list(request) :
      page = "pages/tax_types.html"
      taxes = TaxTypes.objects.all()
      if request.GET.get("init") :
            return redirect("e_init_tax_types")
      content = {"taxes" : taxes}
      return render(request ,page ,content)


def tax_sub_type_list(request) :
      page = "pages/tax_types.html"
      taxes = TaxSubtypes.objects.all()
      if request.GET.get("init") :
            return redirect("e_init_tax_sup_types")
      content = {"taxes" : taxes}
      return render(request ,page ,content)
def init_tax_sup_types(request):
    #tax table items
    url = "https://sdk.invoicing.eta.gov.eg/files/TaxSubtypes.json"
    re = requests.get(url)
    subtypes = re.json()
 
    for i in  range(0,len(subtypes)):
        # try:
            a = TaxSubtypes(Code=subtypes[i].get("Code"),
                            Desc_en=subtypes[i].get("Desc_en"),
                            Desc_ar=subtypes[i].get("Desc_ar"),
                            TaxtypeReference=TaxTypes.objects.filter(
                                Code=subtypes[i].get("TaxtypeReference")).first()
                            )
            a.save()
            print(a)


 
    return redirect("e_tax_sub_type_list")

def init_tax_types(request):
    # f = open("taxtypes.json")
    # json_data = json.load(f)
    url = "https://sdk.invoicing.eta.gov.eg/files/TaxTypes.json"
    re = requests.get(url)
    subtypes = re.json()
 
    for i in  range(0,len(subtypes)):
        # try:
            a  , create= TaxTypes.objects.get_or_create(Code=subtypes[i].get("Code"),
                            Desc_en=subtypes[i].get("Desc_en"),
                            Desc_ar=subtypes[i].get("Desc_ar"),
                         
                            
                            )
            a.save()
            print(a)


    # non tax table items 
    end_point = "https://sdk.invoicing.eta.gov.eg/files/NonTaxableTaxTypes.json"
    re_n = requests.get(end_point)
    subtypes_n = re_n.json()
    for i in  range(0,len(subtypes_n)):
        # try:
            a,create = TaxTypes.objects.get_or_create(Code=subtypes_n[i].get("Code"),
                            Desc_en=subtypes_n[i].get("Desc_en"),
                            Desc_ar=subtypes_n[i].get("Desc_ar"),
                           
                               
                            )
            a.save()
            print(a)
    return redirect("e_tax_type_list")
@api_view(['GET'])
def get_invoice_json(request):
    invoice, created = Receiept.objects.get_or_create()
    seller, created = Seller.objects.get_or_create()
    # discount, created = DiscountObj.objects.get_or_create()
    
    item_data, created = itemData.objects.get_or_create()


    taxType , created = TaxTypes.objects.get_or_create(
        Code = "T1"
    )
    subType , created = TaxSubtypes.objects.get_or_create(
        Code = "V009",
        TaxtypeReference = taxType
    )

    # print("item_data ========> ", item_data)


    # Invoice Data
    invoice.dateTimeIssued = "2022-12-28T14:01:21Z" #datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    invoice.receiptNumber = "12ss3415855"
    invoice.uuid = ""
    invoice.previousUUID = ""
    invoice.referenceOldUUID = ""
    invoice.currency = "EGP"
    invoice.exchangeRate = 0
    invoice.sOrderNameCode = "sOrderNameCode"
    invoice.orderdeliveryMode = ""
    invoice.grossWeight = 6.58
    invoice.netWeight = 6.89

    # documentType
    invoice.receiptType = "S"
    invoice.typeVersion = "1.2"
    

    # seller
    seller.rin = "636346196"
    seller.companyTradeName =  "ديناميك بيزنس سوليوشن للبرمجيات"
    seller.branchCode = "0"
    seller.deviceSerialNumber = "478963214785"
    seller.syndicateLicenseNumber = "C"
    seller.activityCode = "6920"

    # branchAddress
    seller.country = "EG"
    seller.governate = "cairo"
    seller.regionCity = "city center"
    seller.street = "16 street"
    seller.buildingNumber = "14BN"
    seller.postalCode = "74235"
    seller.floor = "1F"
    seller.room = "3R"
    seller.landmark = "tahrir square"
    seller.additionalInformation = "talaat harb street"
    invoice.seller = seller



    # buyer 
    invoice.buyer_type = "F"
    invoice.buyer_id = "313717919"
    invoice.buyer_name = "taxpayer 1"
    invoice.buyer_mobileNumber = "+201020567462"
    invoice.buyer_paymentNumber = "987654"

    # itemData 
    item_data.internalCode = "880609"
    item_data.description = "Samsung A02 32GB_LTE_BLACK_DS_SM-A022FZKDMEB_A022 _ A022_SM-A022FZKDMEB"
    item_data.itemType = "GS1"
    item_data.itemCode = "037000401629"
    item_data.unitType = "EA"
    item_data.quantity = 35
    item_data.unitPrice =  247.96
    item_data.netSale = 7810.74
    item_data.totalSale = 8678.6
    item_data.total = 8887.0436
    item_data.valueDifference = 20


    

    # commercialDiscountData

    commercialDiscountData,created = DiscountObj.objects.get_or_create(
        amount = 867.86 ,
        description = "XYZ"
    )
    item_data.commercialDiscountData.clear()
    item_data.commercialDiscountData.add(commercialDiscountData)



    # itemDiscountData

    itemDiscountData1,created = DiscountObj.objects.get_or_create(
        amount = 10 ,
        description = "ABC"
    )

    itemDiscountData2,created = DiscountObj.objects.get_or_create(
        amount = 10 ,
        description = "XYZ"
    )
    item_data.itemDiscountData.clear()
    item_data.itemDiscountData.add(itemDiscountData1)
    item_data.itemDiscountData.add(itemDiscountData2)




    # taxableItems
    
    taxes, created = taxableItems.objects.get_or_create(
        taxType = taxType ,
        amount = 1096.3036 ,
        subType = subType,
        rate = 14 ,
    )

    item_data.taxableItems.clear()
    item_data.taxableItems.add(taxes)

    # End itemData
    item_data.save()
    
    invoice.itemData.clear()
    invoice.itemData.add(item_data)



    # Totals

    invoice.totalSales = 8678.6
    invoice.totalCommercialDiscount = 867.86
    invoice.totalItemsDiscount = 20
    invoice.netAmount = 7810.74000
    invoice.feesAmount = 0
    invoice.totalAmount = 8887.0436
    invoice.paymentMethod = "C"
    invoice.adjustment = 0

    # extraReceiptDiscountData
    extraReceiptDiscountData,created = DiscountObj.objects.get_or_create(
        amount = 0 ,
        description = "ABC"
    )
    invoice.extraReceiptDiscountData.clear()
    invoice.extraReceiptDiscountData.add(extraReceiptDiscountData)

    
    # Tax Totals  taxTotals



    taxes_total, created = taxTotals.objects.get_or_create(
        amount= 1096.3036,
        taxType=taxType.Code
    )
    taxes_total.save()
    invoice.taxTotals.clear()
    invoice.taxTotals.add(taxes_total)
    serializer = ReceieptSerializer(invoice)
    invoice.set_invoice_uuid(serializer.data)
    invoice.save()

    # print(invoice.__dict__)
    

    # invoice.uuid = get_invoice_uuid(serializer.data) 
    serializer = ReceieptSerializer(invoice)
    return Response(serializer.data)


def home(request):
    page = "home.html"
    return render(request, page)
