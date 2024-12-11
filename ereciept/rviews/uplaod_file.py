from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import JsonResponse
from ereciept.models.uplload_sheet import Sheet
import ereciept.models as tables
from .utils import get_json_object
import datetime
import json
from .reciept import get_seller_data ,round_double,object_to_post ,get_periosue_uuid
from ereciept.utils import get_invoice_uuid

Receiept    = tables.Receiept
TaxTemplate = tables.TaxTemplate
itemData    = tables.itemData
DiscountObj = tables.DiscountObj

columname = [
"dateTimeIssued" , "receiptNumber" , "currency" , "exchangeRate" , "sOrderNameCode" , "orderdeliveryMode" ,"grossWeight",
"buyertype" ,"buyerid" ,"buyername" ,"buyermobileNumber","paymentNumber","paymentMethod" , "extraDiscountAmount" ]
items_cols=[
"internalCode(item)" ,"description(item)" ,"itemType(item)" ,"itemCode(item)" ,"unitType(item)" ,"quantity(item)" ,"unitPrice(item)",
"taxableItems(item)" , "itemDiscountData(amount)" , "itemDiscountData(description)","rd_tax"

]
def upload_file(request) : 
    a = Sheet(
         file =request.FILES['myfile'])
    a.save()
    data = pd.read_excel( a.file.path  ,sheet_name = 0 )
    dat_list = []
    dict_data = {}
    # key = itemCode(item)
    for id in range(0 , len(data['itemCode(item)'])) :
        items_list = []
        items_data = {}
        try :
            idxc =  data['receiptNumber'].iloc[id] 
        except:
            print("error ")
            return  JsonResponse({"erro" : 'Plaes set Internal id correctly'})
        if  str(data['receiptNumber'].iloc[id]) !='nan' and data['receiptNumber'].iloc[id] :
            items_list = []
            dict_data = {}
            for col_name in columname :
                try :
                     dict_data[col_name] = str(data[col_name].iloc[id]) if str(data[col_name].iloc[id] )!= 'nan' else " "
                except:
                    print ({"erro" : col_name +'  - not found'})
                    pass
            for item in items_cols :
                if item in data.keys():
                    try :
                         items_data[item] =str( data[item].iloc[id] )if str(data[item].iloc[id]) != 'nan' else " "
                    except :
                        pass

            items_list.append(items_data)   
            if len(items_list) > 0 :
                dict_data['items'] = items_list
                dat_list.append(dict_data)
        if  str(data['receiptNumber'].iloc[id]) =='nan' and str(data['itemCode(item)'].iloc[id] )!= 'nan' :
            items_data ={}
            for item in items_cols :
                if item in data.keys():
                    if data[item].isnull ==False:
                        items_data[item] = str(data[item].iloc[id]) if str(data[item].iloc[id]) != 'nan' else " " 
            items_list.append(items_data)
            if len(items_list) > 0 :
                for i in items_list : 
                  dict_data['items'].append (i)
    data_json = json.dumps(dat_list)
    
           
    return JsonResponse({"invoices" :dat_list })



def craete_reciept_api(request) :
    data_res  = json.load(request)
    data = data_res.get("data")
    if not data :
        print("Error No data in craete_reciept_api")
        return JsonResponse({"error" :"No data found "})
    local_number = str(data.get("receiptNumber").split('.')[0])
    exchangeRate = data.get("exchangeRate") 
    localRate =1
    # print(data)
    if exchangeRate  and exchangeRate != " ":
       localRate = float(data.get("exchangeRate") )
    date_time_issued = data.get("dateTimeIssued")
    reciept = Receiept (
            dateTimeIssued  = date_time_issued  ,
            receiptNumber   = local_number , 
            currency        = data.get("currency") if data.get("currency") and len(data.get("currency")) > 2 else "EGP" ,
            exchangeRate    =  localRate ,
            buyer_id        = str(data.get("buyerid") or " ") if  len( str(data.get("buyerid") or " ")) > 2 else " " ,
            buyer_name      = str(data.get("buyername") or " ")   , 
            buyer_type      = str(data.get("buyertype") or "  ")    if len( str(data.get("buyertype") or "   ") )  == 1 else "P"     , 
            buyer_mobileNumber = str(data.get("buyermobileNumber") or " ")  ,
            buyer_paymentNumber = str (data.get("paymentNumber") or " ")
    )
    try :
        reciept.save()
    except Exception as E :
        return JsonResponse({f"Error " : f"Error in  reciept number {local_number}"  +str(E)})
    for item in data.get("items") :

        
        #create item andd add to reciept 
        qty =float (item.get("qty") or 1)
        price = float(item.get("unitPrice(item)") or 1)
        template = TaxTemplate.objects.filter(name= str(item.get("taxableItems(item)")) ).first()
        print("template" , str(item.get("taxableItems(item)")) ,template)
        i = itemData(
            internalCode = item.get("internalCode(item)") , 
            description  = item.get("description(item)") , 
            itemType  = item.get("itemType(item)") , 
            itemCode = item.get("itemCode(item)") ,
            unitType = item.get("unitType(item)") , 
            quantity = qty  ,
            unitPrice = price , 
            parent =  reciept.id,
            rd_tax = float(item.get("rd_tax") or 0)

        )
        i.save()

        if item.get("itemDiscountData(amount)") and float(item.get("itemDiscountData(amount)") or 0) > 0:
            #create discount object
            a = DiscountObj(
                amount      = float(item.get("itemDiscountData(amount)") ), 
                description =  item.get("itemDiscountData(description)")
            )
            a.save()

            i.commercialDiscountData.add(a)
            i.save()


        try :
             i.save()
        except Exception as e :
              return JsonResponse({f"Error" :f" in  item Code  {item.get('itemType(item)')}"+ str(e)})
        if template :
            i.taxtemplate = template
            try :
                  i.save()
            except Exception as e :
                    return JsonResponse({f"Error" :f" in  item Code  {item.get('itemType(item)')}"+ str(e)})
        try :
             i.save()
        except Exception as e :
             return JsonResponse({f"Error" :f" in  item Code  {item.get('itemType(item)')}"+ str(e)})

        i.save()
        reciept.itemData.add(i)
        reciept.docstatus = "0" 
        try :
                 reciept.save()
        except Exception as E :
                return JsonResponse( {f"Error" : f"Error in  reciept number {local_number}"  +str(E)})
    try :
       data =  post_to_portal( reciept.id )
       return JsonResponse({"Success" : data,"status":"1"})
    except Exception as E :
         return JsonResponse({f"Error" : f"Error in  reciept number {local_number}"  +str(E),"status":"0"})
    
    return JsonResponse({"name" : reciept.receiptNumber })

def post_to_portal( pk):
 
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
        itemDiscountData = form["itemData"][0]["itemDiscountData"]
        for c_discount in item.itemDiscountData.all() :
            print("c_discount.amount" , c_discount.amount)
            itemDiscountData["amount"] = round_double(c_discount.amount)
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
    # form["extraReceiptDiscountData"] = [{"amount":10000.0 , "description" : "Extra Discount"}]
    form["netAmount"] =round_double( reciept.netAmount )
    form["feesAmount"] = round_double(reciept.feesAmount)
    form["totalAmount"] = round_double(reciept.totalAmount )
    form["paymentMethod"] = reciept.paymentMethod or "C"
    # tax total 
    taxTotals =[  {"taxType" :k, "amount" :v} for k,v in tax_totals.items()]


   
    
    form["taxTotals"] = taxTotals  
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
    return {"status":reciept.status,"number":reciept.receiptNumber}