from django.shortcuts import render ,redirect ,get_object_or_404

from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Page, Paginator

import ereciept.models as tables
from base64 import b64encode
import urllib
# data for e-tax 
import json
import requests
from ereciept.serializer import  ReceieptWithoutUUIDSerializer
from ereciept.utils import get_invoice_uuid
from ereciept.models.masterData import itemTypeChoisec ,unitTypeChoices
Receiept = tables.Receiept
TaxTemplate = tables.TaxTemplate
itemData = tables.itemData

data_urls = {
        "production" :{"login" :"https://id.eta.gov.eg" , "portal" :"https://api.invoicing.eta.gov.eg"} , 
        "preproduction" : {"login" :"https://id.preprod.eta.gov.eg" , "portal" :"https://api.preprod.invoicing.eta.gov.eg"}
    }
def seller_token():
    Seller = tables.seller.Seller
    seller = Seller.objects.filter(current_s =1).first()
    api_key = seller.api_key
    api_secret = seller.api_secret
    login_url  = data_urls[ "production"].get("login") if seller.enviroment =="production" else  data_urls[ "preproduction"].get("login")
    method= '/connect/token'
    url = login_url + method
    grant_type = 'client_credentials'
    srta = f"{str(api_key)}:{str( api_secret)}"
    str_byte = bytes(srta, 'utf-8')
    userAndPass = b64encode(str_byte).decode("ascii")
    # body = 'grant_type=%s'%grant_type
    body = {
            "grant_type" :"client_credentials" ,
            "client_id":api_key ,
            "client_secret":api_secret
            }
    headers = { 
          "Content-Type":"application/x-www-form-urlencoded",
          "Connection":"keep-alive",
          "Accept":'*/*',
          'Accept-Encoding':'gzip, deflate, br',
          "posserial" :seller.deviceSerialNumber ,
            "pososversion" :seller.pososversion 
          }
    try :
        r= requests.post(url , headers=headers , data=urllib.parse.urlencode(body))
        data = r.json() 
        token = data.get("access_token")
   
        return token
    except :
        return False


def get_seller_data():
    Seller = tables.seller.Seller
    seller = Seller.objects.filter(current_s =1).first()
    return seller
def new_reciept(request):
    receiept = Receiept(
         postingdate = datetime.now()
    )
    receiept.docstatus = '-1'
    receiept.save()
    return redirect(receiept.get_absolute_url())
    page =  "pages/reciept.html"
    return render(request ,page  )


def get_reciept(request ,pk) :
    units= list(unitTypeChoices)
    units_obj = [{"id" :unit[0] , "name" :unit[1]} for unit in units ]
    #receiept =get_object_or_404(Receiept , slug = slug)
    receiept =Receiept.objects.filter( pk = pk).first()
    page =  "pages/reciept.html"
    taxes = TaxTemplate.objects.all()
    
    
    content = {
        "receiept" :receiept ,
        "taxes" :taxes ,
        "units" :units_obj
    }
    return render(request ,page ,content )
def post_receipt_data(request):
    if request.method != "POST" :
        return JsonResponse({"message": "Error method"})
    data = request.POST
   
    receipt_id             = data.get("r_id")
    receiept               = get_object_or_404(Receiept , id = receipt_id)
    receiept.receiptNumber =  data.get("receiptNumber") 
    receiept.buyer_type    = data.get("buyer_type")
    receiept.buyer_id      = data.get("buyer_id")
    receiept.buyer_name    = data.get("buyer_name")
    receiept.buyer_mobileNumber  = data.get("buyer_mobileNumber")
    receiept.buyer_paymentNumber = data.get("buyer_paymentNumber")
    receiept.dateTimeIssued = data.get("dateTimeIssued")
    receiept.docstatus = "0"
    receiept.save()
    return redirect(get_reciept , pk =receiept.id)
def add_receiept_item(request) :
    if request.method != "POST" :
        return JsonResponse({"message": "Error method"})

    data = request.POST
    receipt_id = data.get("r_id")

    receiept =get_object_or_404(Receiept , id = receipt_id)
  
    a = itemData(
        internalCode = data.get("internalCode") ,
        description = data.get("description") , 
        itemType = data.get("itemType") ,
        itemCode = data.get("itemCode") ,
        quantity = data.get("stock_qty") ,
        unitType = data.get("stock_uom") ,
        unitPrice = data.get("rate")

    )
    # print(a)
    a.save()
    a.parent = receiept.id
    a.save()
    receiept.itemData.add(a)
    #a.save()
    receiept.docstatus = "0"
    receiept.save()
    # for item in receiept.itemData.all() :
    #     item.parent = receiept.id  
    #     if data.get("taxtemplate") :
    #         item.taxtemplate = TaxTemplate.objects.filter( pk=data.get("taxtemplate")).first()
    #     item.save()
    receiept.save()
    # data = reciept_update_data( receiept.id)
    #return JsonResponse(data, safe=False)
    return redirect(get_reciept , pk =receiept.id)

def edit_receiept_item(request) :
    if request.method != "POST" :
        return JsonResponse({"message": "Error method"})

    data = request.POST
    print("data:",data)
    
    line_id = data.get("line_id")
    line = get_object_or_404(itemData ,id =  line_id)
    
    line.internalCode = data.get("internalCode") 
    line.description = data.get("description")  
    line.itemType = data.get("itemType") 
    line.itemCode = data.get("itemCode") 
    line.quantity = data.get("stock_qty")
   
    line.unitType = data.get("stock_uom") 
    line.unitPrice = data.get("rate")
  
    if data.get("taxtemplate") :
          line.taxtemplate = TaxTemplate.objects.filter( pk=data.get("taxtemplate")).first()
    line.save()
    receiept = Receiept.objects.get(pk = line.parent)

    
    receiept.save()
    
   
    return redirect(get_reciept, pk=receiept.id)

#### add method to call 



def round_double(x=0):
    return abs(round((x or 0), 4))

def create_invocie_json( request ,pk):
    from .utils import get_json_object
    import datetime
    reciept = Receiept.objects.get(id = pk)
    form = get_json_object() 
    #set form header 
    timer = reciept.dateTimeIssued
    data_time = reciept.dateTimeIssued.split('.')
    if len(data_time) >= 2 :
        print(len(data_time)) 
        timer = data_time[0] + data_time[1][-1]
    if len(data_time) == 1 :
         timer = data_time[0]
    
    header = form["header"]
    header["dateTimeIssued"] =timer#"2023-02-27T13:33:47Z" #timer
    header["receiptNumber"] = reciept.receiptNumber
    header["currency"] = reciept.currency
    per_uuid = get_periosue_uuid()
    if per_uuid :
      header["previousUUID"] =   per_uuid
    form["header"] = header
    
    # header end 
    
    # *** set seller *** 
    current_seller = get_seller_data()
    if not current_seller :
        return JsonResponse({"Error": "No Seller Found "}) 
    seller = form["seller"]
    seller["rin"]                =  current_seller.rin
    seller["companyTradeName"]   =  current_seller.companyTradeName
    seller["branchCode"]         = current_seller.branchCode
    seller["deviceSerialNumber"] = current_seller.deviceSerialNumber
    seller["activityCode"]       = current_seller.activityCode
    branch_address = form["seller"]["branchAddress"]
    branch_address["governate"]      = current_seller.governate
    branch_address["regionCity"]     = current_seller.regionCity
    branch_address["street"]         = current_seller.street
    branch_address["buildingNumber"] = current_seller.buildingNumber
    seller["branchAddress"]          = branch_address
    form["seller"] = seller
    form["documentType"] = {"receiptType" :reciept.receiptType  , "typeVersion" :"1.2"}

    #***  seller end ***

    # *** set Buyer ***
    buyer = form["buyer"]
    buyer["type"]  = reciept.buyer_type
    buyer["id"] =reciept.buyer_id  or "None"
    buyer["name"] = reciept.buyer_name or "None"
    buyer["mobileNumber"] = reciept.buyer_mobileNumber or "None"
    buyer["paymentNumber"] = reciept.buyer_paymentNumber or "None"
    form["buyer"] = buyer
    # *** buyer End ***

    #*** start item ***
    tax_totals ={}
    itemData = []
    for item in reciept.itemData.all() :
        itemForm ={}
        itemForm["internalCode"] =item.internalCode
        itemForm["itemCode"] = item.itemCode
        itemForm["description"]  =item.description
        itemForm["itemType"]     = item.itemType
        itemForm["unitType"]     = item.unitType
        itemForm["quantity"]     = round_double(item.quantity) #float(item.quantity or 0)
        itemForm["unitPrice"]    = round_double(item.unitPrice )
        itemForm["netSale"]      = round_double(item.netSale)
        itemForm["totalSale"]    = round_double(item.totalSale )
        itemForm["total"]        = round_double(item.total)
        itemForm["commercialDiscountData"] = []
        itemForm["itemDiscountData"] = []
        commercialDiscountData = {}
        for c_discount in item.commercialDiscountData.all() :
            commercialDiscountData["amount"] = round_double(c_discount.amount)
            commercialDiscountData["description"] = c_discount.description
            itemForm["commercialDiscountData"].append(commercialDiscountData)
        itemDiscountData ={}
        for c_discount in item.itemDiscountData.all() :
            print("amount" ,c_discount.amount)
            itemDiscountData["amount"] =float(c_discount.amount or 0)
            itemDiscountData["description"] = c_discount.description
            itemForm["itemDiscountData"].append(itemDiscountData)
        
        
        formtaxableItems= []
        
        for tax in item.taxableItems.all() :
            taxableItems = {}
            taxableItems["taxType"] = tax.taxType.Code
            if  tax.taxType.Code in tax_totals.keys() :
                tax_totals[tax.taxType.Code] = round_double(tax_totals.get(tax.taxType.Code)) + round_double(tax.amount)
            if  tax.taxType.Code not in tax_totals.keys() :
                tax_totals[tax.taxType.Code] = round_double(tax.amount)
            taxableItems["amount"] = round_double(tax.amount)
            taxableItems["subType"] = tax.subType.Code if tax.subType else " "
            taxableItems["rate"] = round_double(tax.rate)
            formtaxableItems.append( taxableItems) 

        itemForm["taxableItems"] = formtaxableItems
        itemData.append(itemForm)



    form["itemData"] = itemData 
    #*** enditem ***


    #footer total
    form["totalSales"] =  round_double(reciept.totalSales)
    form["totalCommercialDiscount"] = reciept.totalCommercialDiscount
    form["totalItemsDiscount"] = reciept.totalItemsDiscount
    extraReceiptDiscountData  = []
    for disc in reciept.extraReceiptDiscountData.all() :
        discount_form = form["extraReceiptDiscountData"][0]
        discount_form["amount"] = round_double(disc.amount)
        discount_form["description"] = disc.description
        extraReceiptDiscountData.append(discount_form)
    form["extraReceiptDiscountData"] = extraReceiptDiscountData
    form["netAmount"] =round_double( reciept.netAmount )
    form["feesAmount"] = round_double(reciept.feesAmount)
    form["totalAmount"] = round_double(reciept.totalAmount )
    form["paymentMethod"] = reciept.paymentMethod or "C"
    # tax total 
    taxTotals =[  {"taxType" :k, "amount" :v} for k,v in tax_totals.items()]


   
    
    form["taxTotals"] = taxTotals  
    if reciept.referenceOldUUID :

             form["header"]["referenceUUID"]  = reciept.referenceOldUUID
    
    #taxTotals
    reciept.uuid = get_invoice_uuid(form)
   
    # reciept.save()
    form["header"]["uuid"] = reciept.uuid
    
    
    data= object_to_post(form)
    accepted = data.get("Success")
    if accepted :
        reciept.submitionid = accepted.get('submissionId')
        if  accepted.get('acceptedDocuments') :
            reciept.status = "Submit"
            reciept.t_uid  =  accepted.get('acceptedDocuments')[0].get('uuid')
            reciept.docstatus = "1"
            reciept.save()
        if  accepted.get('rejectedDocuments') :
            reciept.status = "reject"
            reciept.docstatus = "0"
            reciept.submitionid  =accepted.get('rejectedDocuments')[0].get('error').get("details")
           
        reciept.save()
    
    reciept.save()
    return redirect(get_reciept , pk =reciept.id)
def create_invocie_json_return(request,pk):
    receiept = Receiept.objects.filter(
         pk=pk
    ).first()
  
    item_list = [item for item in receiept.itemData.all()]
    receiept.referenceOldUUID = receiept.uuid
    receiept.pk = None
    receiept.serial_number = None
    receiept.slug = None
    receiept.uuid = None
    receiept.t_uid = None
    receiept.is_return = True
    receiept.docstatus = '0'
    receiept.save()
    for i in item_list :
        a = itemData.objects.get(id = i.id )
        a.pk = None
     
        a.save()
        a.parent = receiept.id
        a.save()
        receiept.itemData.add(a)
        receiept.save()
    
    return redirect(receiept.get_absolute_url())
#ereciept.rviews.reciept  
def get_periosue_uuid():
    old_uid = Receiept.objects.filter(status="Submit").order_by("-id")
    seller = get_seller_data()
    tok = seller_token()
    headers = {
                    "Authorization"   : 'Bearer %s'%tok,
                    "Accept"          : "application/json" ,
                    "Accept-Language" : "en" ,
                    'Content-Type'    :'application/json' 
                    }
    for old in old_uid :
       
        #validate uid fofr last invocie 
        uid_url = f"/api/v1/receipts/{old.t_uid}/details"
        url = data_urls[ "production"].get("portal") if seller.enviroment =="production" else  data_urls[ "preproduction"].get("portal")
        c = requests.get(url+ uid_url ,headers=headers )
        if c.status_code ==200 :
            return old.t_uid
        return False


from django.core import serializers
from rest_framework import serializers

class taxTemplateSerializer(serializers.ModelSerializer):
    class Meta :
        model =  TaxTemplate 
        fields = ["name" , "id"]
class itemDataSerializer(serializers.ModelSerializer):
    taxtemplate =  taxTemplateSerializer(many=False)
    class Meta:
        model = itemData
        fields="__all__"
def reciept_update_data(reciept_id) :
    reciept = Receiept.objects.filter(id = reciept_id).first()
    items = reciept.itemData.all().values()
    total_sales = reciept.totalSales
    total_amount = reciept.totalAmount
    data = {"items" :list( items) ,"total_sales":total_sales ,"total_amount" :total_amount}
    return data
def delete_reciept_line(request):
    data = json.load(request)
    line_id   = data.get("line_id")
    reciept_id= data.get("reciept_id")
    if  line_id and reciept_id:    
        item_line = itemData.objects.filter(id = line_id).first()
        reciept = Receiept.objects.filter(id = reciept_id).first()
        reciept.itemData.remove(item_line)
        item_line.delete()
        reciept.save()
        updates = reciept_update_data(reciept_id)
        return JsonResponse(updates , safe=False)
    return JsonResponse({"error" : f"Data error in line_id : {line_id} or reciept_id : {reciept_id}"})
def reciept_line_details(request , pk) :
    line = itemData.objects.get(id=pk)
    
    serializer = itemDataSerializer(line)
    print("reciept_line_details:",serializer)
   
    return JsonResponse( serializer.data )
def object_to_post(inv):
    receipts = []
    seller = get_seller_data()
    data = {
        "receipts" :[inv] ,
        # "signatures" : []
    }
    tok = seller_token()
    headers = {
                    "Authorization"   : 'Bearer %s'%tok,
                    "Accept"          : "application/json" ,
                    "Accept-Language" : "en" ,
                    'Content-Type'    :'application/json' 
                    }
    try :
        url = data_urls[ "production"].get("portal") if seller.enviroment =="production" else  data_urls[ "preproduction"].get("portal")
        method = "/api/v1/receiptsubmissions"
        c = requests.post(url+method ,headers=headers , data=json.dumps(data , ensure_ascii=0).encode("utf-8").decode('unicode-escape'))
        #c = requests.post(url+method ,headers=headers , data=json.dumps(data ).encode("utf-8"))
        res = c.json()
        if c.status_code == 202 :
            return ({"Success":res})
        if c.status_code != 202 :
            return {"Token Error" : {"status" :str(res.status)  , "Error" :str( res)}}
    except Exception as E :
        print(E)
        return {"Token Error" : str(E) }
