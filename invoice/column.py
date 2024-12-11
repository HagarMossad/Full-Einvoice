from payer.models import PayerAccount
import subprocess
import pandas as pd
import json
import requests
from .models import EInvoice
from tax.models import TaXCategory, taxableItems ,TaxTotals
from http.client import HTTPSConnection
from base64 import b64encode
import ssl
import os
columns = ['Series',
'Type',
'Document Type',
'Receiver Type',
'Receiver',
'Receiver Id',
'Receiver Name',
'Receiver branchID',
'Receiver Country',
'Receiver Region City',
'Receiver Governate',
'Receiver Street',
'Receiver Building Number',
'Date TimeIssued',
'Internal Id',
           ]

items_cols = [
                'Code (Item)',
                'Description (Item)',
                'UOM (Item)',
                'Item Type (Item)',
                'QTY (Item)',
                'Rate (Item)',
                'Discount (Item)',
                'Item Tax (Item)',
                'amountSold(Item)' ,
                'currencySold(Item)' , 
                'currencyExchangeRate(Item)' , 
                'Tax Amount']



def post_to_auth_upload(id):
    from reports.views import get_token
    invoice  = EInvoice.objects.filter(id=id).first()
    if not invoice :
        return ({'error' : "Invocie Id Error "})
    form = { "documents":[{
        "issuer":{ 
									 "name"   : invoice.issuer_name ,
									 "id"     : invoice.issuer_id or "",
									 "type"   : invoice.issuer_type  ,
									 "address": {
									 			   "branchID"      :invoice.issuer_address_branchId or ''  ,
                                                    "country"    :invoice.issuer_address_country or '' ,
							 			           "governate"     :invoice.issuer_address_governate or ''  ,
                                                   "regionCity" : invoice.issuer_address_regionCity or '' ,
							 			           "street"        :invoice.issuer_address_street     ,
								  				   "buildingNumber":str(invoice.issuer_address_buildingNumber or '')
								  				
		
												} 
                } ,
         "receiver":{ 
									 "name"   : invoice.receiver_name ,
									 "id"     : invoice.receiver_id or "",
									 "type"   : invoice.receiver_type  ,
									 "address": {
									 			   "branchID"      :invoice.receiver_address_branchId or ''  ,
                                                    "country"    :invoice.receiver_address_country or '' ,
							 			           "governate"     :invoice.receiver_address_governate or ''  ,
                                                   "regionCity" : invoice.receiver_address_regionCity or '' ,
							 			           "street"        :invoice.receiver_address_street     ,
								  				   "buildingNumber":str(invoice.receiver_address_buildingNumber or '')
								  				
		
												} 
                } ,
        #main info Section 
        "documentType"             :invoice.documentType,
        "documentTypeVersion"      :str(invoice.documentTypeVersion), 
        # 2021-05-17 12:21:11
        "dateTimeIssued"            :invoice.datetimestr ,
        "taxpayerActivityCode"     : str(invoice.taxpayerActivityCode ) ,
        "internalID"               : str(invoice.internalId or ''),
        "purchaseOrderReference"   : "",#str(self.purchase_order_reference or ''),
        "purchaseOrderDescription" : "" ,
        "salesOrderReference"      : "" ,
        "salesOrderDescription"    : "" ,
        "proformaInvoiceNumber"    : "" ,
        

        #Item section 
        "invoiceLines" :[ {
		              'description'     :item.description,
		              'itemType'        :item.itemType,
		              'itemCode'        :item.itemCode,
		              'unitType'        :item.unitType,
		              'quantity'        :float(item.quantity),
		              'internalCode'    :item.itemCode,
		              'salesTotal'      :round(float(item.salesTotal or 0 ) ,5),
		              'total'           :round( float(item.total or 0) , 5) ,
		              'valueDifference' :float(item.valueDifference or 0) , 
		              'totalTaxableFees':0, #round(float(item.totalTaxableFees or 0 ) , 5) ,#float(item.total_taxable_fees or 0),
		              'netTotal'        :round(float(item.netTotal or 0) , 5 )  ,
		              'itemsDiscount'   : 0, #round((item.item_discount * item.quantity) , 5),
		              'unitValue'       :   {
		                                    'currencySold'        :item.unitValue_currencySold,
		                                    'amountEGP'           :round(float(item.unitValue_amountEGP) , 5),
		                                    'amountSold'          :round(float(item.unitValue_amountSold or 0) , 5) if item.unitValue_currencySold != 'EGP' else 0,
		                                    'currencyExchangeRate': round(float(item.unitValue_currencyExchangeRate or 1 ) , 5) if item.unitValue_currencySold != 'EGP' else 0,
		                                    },
		              'discount'        :  {
		                                   'rate':0,
		                                    'amount':round((float(item.discount_amount  or 0)  ), 5)
		                                    },

                        "taxableItems" :[ {"taxType":tax_i.taxType ,
                                           "amount": abs(round(float(tax_i.amount or 0 ) , 5)) ,
                                            "subType" : tax_i.subType ,
                                            "rate" :abs(round( float ( tax_i.rate or 0) , 5 ))}
                                             for tax_i in  item.taxableItems.all()]
                     
		             
		   	 }


         for item in  invoice.invoiceLines.all()] , 

        #total Section 
        "totalDiscountAmount"      :float(invoice.totalDiscountAmount or 0),
        "totalSalesAmount"         :float(invoice.totalSalesAmount or 0) ,
        "netAmount"                :float(invoice.netAmount or 0),
        "taxTotals"                : [
            {
                "taxType" : tax_e.taxType ,
                "amount" : abs(round( float (tax_e.amount or 0),5))
            }
        for tax_e in  
        invoice.taxTotals.all()],#invoice.taxTotals.all(),
        "totalAmount"              :float(invoice.totalAmount or 0)   ,
        "extraDiscountAmount"      :0,
        "totalItemsDiscountAmount" :0 ,


		


    }]
    }
    token = get_token()
    headers = {
				"Authorization"   : 'Bearer %s'%token,
				"Accept"          : "application/json" ,
				"Accept-Language" : "ar" ,
				'Content-Type'    :'application/json' 
				 }

    import sys
    
    if invoice.documentTypeVersion == "0.9"  :
        print(invoice.documentTypeVersion )
        c = HTTPSConnection('api.preprod.invoicing.eta.gov.eg' ,context=ssl._create_unverified_context())
        c.request('POST', '/api/v1.0/documentsubmissions' ,headers=headers , body=json.dumps(form) )
        res = c.getresponse()
        data = res.read()
        return ({'message' : str(data)})
    if invoice.documentTypeVersion == "1.0"  :
        print("formmmmmmmmmmmmmyyyyyy",form)
        main_data={}
        try :
          os.remove('C:/j/sFile.txt')
        except:
            pass
        jsonfile = "C:/j/sFile.txt"
        str_form = json.dumps(form.get('documents')[0])
        print(" form" , str_form)
        with open(jsonfile, 'a', encoding='utf-8') as outfile:
            json.dump(form.get('documents')[0], outfile )

        cmd = 'C:/j/EInvoicingSigner.exe'
        result = subprocess.Popen([cmd ,' '], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a,b = result.communicate()
        print(a,b)
        if a :

            h = json.loads(a)
            if h.get('submissionId') :
                accepted_document = { "submissionId" :h.get('submissionId') }
                # if h.get('submissionId') : 
                #     main_data['submissionId'] =  h.get('submissionId')
                # self.request.sendall(json.dumps(accepted_document).encode('utf-8'))
                return ({'message' : str(accepted_document)})

            else :
                try :
                  rejected = h.get('rejectedDocuments')[0].get('error').get('details')[0]
                  main_data['error_details'] =rejected or b
                  return ({'message' : str(main_data)})
                  
                  
                except:
                    main_data['error_details'] =b
                    return ({'message' : str(main_data)})

                  
        else :
            main_data['error_details'] =str(b)
            return ({'message' : str(main_data)})

def create_request(uploader_id , pth):
    data = pd.read_excel( pth  ,sheet_name = 0)
    dat_list = []
    dict_data = {}
    for id in range(0 , len(data['Code (Item)'])) :
        items_list = []
        items_data = {}
        try :
            idxc =  data['Internal Id'].iloc[id] 
        except:
              return {"erro" : 'Plaes set Internal id correctly'}
        if  str(data['Internal Id'].iloc[id]) !='nan' and data['Internal Id'].iloc[id] :
            items_list = []
            dict_data = {}
            for col_name in columns :
                try :
                     dict_data[col_name] = data[col_name].iloc[id] if data[col_name].iloc[id] != 'nan' else " "
                except:
                    return ({"erro" : col_name +'not found'})
            for item in items_cols :
                items_data[item] = data[item].iloc[id]  
            items_list.append(items_data)
            print(items_data)
            if len(items_list) > 0 :
                dict_data['items'] = items_list
                dat_list.append(dict_data)
        if  str(data['Internal Id'].iloc[id]) =='nan' and str(data['Code (Item)'].iloc[id] )!= 'nan' :
            items_data ={}
            for item in items_cols :
                items_data[item] = data[item].iloc[id]  
            items_list.append(items_data)
            if len(items_list) > 0 :
                for i in items_list : 
                  dict_data['items'].append (i)
    response_datat = []

    issuer = PayerAccount.objects.all().first()
    if not issuer :
            return ({"error " : "No Issuer Account Found !"})
   
    issr    = {                              
            "issuer_type"                 :  issuer.issuer_type,
            "issuer_id"                   :   str(issuer.issuer_id),
            "issuer_name"                   : issuer.issuer_name,
            "address"   :{                             
                        "branchID"       :  str(issuer.issuer_address_branchId)  ,
                        "country"        : issuer.issuer_address_country ,
                        "governate"      : issuer.issuer_address_governate,
                        "regionCity"     : issuer.issuer_address_regionCity,
                        "street "        : issuer.issuer_address_street ,
                        "buildingNumber" : str( issuer.issuer_address_buildingNumber)
                        },
            "documentTypeVersion" : str(issuer.documentTypeVersion)
                        
                        
                    } 
  
    for inv in dat_list :
       inv['issuer'] = issr
       inv['taxpayerActivityCode'] = str(issuer.activty_number)
       inv['uploader_id'] = str(uploader_id)
       inv['rd_tax'] = ""
       r_str = str(inv).replace("'" , '"') 
       r_str = str(r_str).replace("nan" , ' " " ')
       status = e_invoice_form( inv)
    
       

    return({"success" :"succes"})



def e_invoice_form(data):
     
        invoice = data
        print(data)
        ic_invoice = EInvoice()
        issuer                                   = invoice.get('issuer')
        ic_invoice.uploader_id                   = str(invoice.get('uploader_id'))
        ic_invoice.issuer_type                   = issuer.get('issuer_type')
        ic_invoice.issuer_id                     = issuer.get('issuer_id')
        ic_invoice.issuer_name                   = issuer.get('issuer_name')
        address                                  = issuer.get('address')
        ic_invoice.issuer_address_branchId       = address.get('branchID')
        ic_invoice.issuer_address_country        = address.get('country')
        ic_invoice.issuer_address_governate      = address.get('governate')
        ic_invoice.issuer_address_regionCity     = address.get('regionCity')
        ic_invoice.issuer_address_street         = address.get('street')
        ic_invoice.issuer_address_buildingNumber = address.get('buildingNumber')
        ic_invoice.receiver_type                   = invoice.get('Receiver Type')
        ic_invoice.receiver_id                     = str(invoice.get('Receiver Id')).split('.')[0]
        ic_invoice.receiver_name                   = invoice.get('Receiver Name') or ''
        # receiver_address                           = invoice.get('receiver_address')
        ic_invoice.receiver_address_branchId       = str(invoice.get('Receiver branchID')).split('.')[0]
        ic_invoice.receiver_address_country        = invoice.get('Receiver Country')
        ic_invoice.receiver_address_governate      = invoice.get('Receiver Governate')
        ic_invoice.receiver_address_regionCity     = invoice.get('Receiver Region City')
        ic_invoice.receiver_address_street         = invoice.get('Receiver Street')
        ic_invoice.receiver_address_buildingNumber = str(invoice.get('Receiver Building Number')).split('.')[0]
        ic_invoice.rd_tax                          = invoice.get('rd_tax')

        # set document info 
        ic_invoice.datetimestr  = invoice.get('Date TimeIssued')
        ic_invoice.documentType = invoice.get('Document Type')
        ic_invoice.documentTypeVersion= str(issuer.get('documentTypeVersion'))
        ic_invoice.taxpayerActivityCode = invoice.get('taxpayerActivityCode')
        ic_invoice.internalId = str(invoice.get('Internal Id')).split('.')[0]
        ic_invoice.save()
        #set Invoice Items 
        invoiceLines = invoice.get('items')
        for line in invoiceLines :
            taxes = line.get('Item Tax (Item)')
            # # taxes_list = [{tax.}]
            tax_cat =  TaXCategory.objects.filter(name =taxes).first()
            currency = line.get('currencySold(Item)') 
            print("currency" , currency )
            exchangerate = 1 
            # if currency == 'nan'  :

            #     currency = 'EGP' 
            if float(line.get('currencyExchangeRate(Item)') or 1 )  != 1:
                 exchangerate = float(line.get('currencyExchangeRate(Item)') or 1 )
            if  tax_cat :
                
                ic_invoice.invoiceLines.create(
                        
                        description = line.get('Description (Item)'),
                        itemType = line.get('Item Type (Item)'),
                        itemCode = line.get('Code (Item)'),
                        unitType = line.get('UOM (Item)') ,
                        quantity = float(line.get('QTY (Item)')),
                        unitValue_currencySold = currency,
                        unitValue_currencyExchangeRate =  float(exchangerate or 1 )if currency !="EGP" else 0  ,#float(line.get('currencyExchangeRate(Item)') or 0 ), 
                        unitValue_amountSold =round(float(line.get('Rate (Item)') or 0 ) ,5 ) if currency !="EGP" else 0 ,
                        unitValue_amountEGP  = round ((round(float(line.get('Rate (Item)') or 1 )  , 5) * float(exchangerate or 1) ) , 5 ),
                        parent_type = "EInvoice" ,
                        parent_id= ic_invoice.id,
                        tax_cat = tax_cat ,
                        discount_amount =float( line.get('Discount (Item)')),
                        rd_tax   = float(line.get('Tax Amount'))



                )
            else:
                ic_invoice.invoiceLines.create(
                    
                        description = line.get('Description (Item)'),
                        itemType = line.get('Item Type (Item)'),
                        itemCode = line.get('Code (Item)'),
                        unitType = line.get('UOM (Item)') ,
                        quantity = float(line.get('QTY (Item)')),
                        unitValue_currencySold = currency,
                        unitValue_currencyExchangeRate =  exchangerate ,#float(line.get('currencyExchangeRate(Item)') or 0 ), 
                        unitValue_amountSold =round(float(line.get('Rate (Item)') or 0 ) ,5 )  ,
                        unitValue_amountEGP  = round ((round(float(line.get('Rate (Item)') or 0 )  , 5) * exchangerate ) , 5 ),
                        parent_type = "EInvoice" ,
                        parent_id= ic_invoice.id,
                        discount_amount =float( line.get('Discount (Item)')),
                      



                )

            ic_invoice.save()
        tax_types = {}
        taxableitem = 0
        for line in ic_invoice.invoiceLines.all():
                total_taxes_fees = 0 
                if line.tax_cat :
                    for tax in  line.tax_cat.tax_table.all() :
                        rate =tax.rate 
                        amount = tax.amount
                        if tax.rate and tax.rate != 0  :
                            amount = (float(line.unitValue_amountEGP or 0) - float(line.discount_amount or 0 )) * (float(rate) / 100 )
                        elif tax.subType == "RD04" or tax.subType == "ST02":
                            amount = float(line.rd_tax or 0)
                            total_taxes_fees += amount
                        if  tax.subType != "ST02":
                            amount=  float(amount or 0) * float(line.quantity or 0)

                        in_tax = taxableItems(taxType = tax.taxType , rate = tax.rate ,
                        subType = tax.subType , amount = round(amount , 4)  , parent_id = line.id , parent_type = 'invoiceLines')
                        for k , v in tax_types.items() :
                                if k ==  tax.taxType :
                                    tax_types[k] = float(v) + float(amount)
                        if tax.taxType  not in  tax_types.keys() :
                            tax_types[tax.taxType] = float(amount) 
                        in_tax.save()
                        line.totalTaxableFees = total_taxes_fees
                        taxableitem += total_taxes_fees
                        line.taxableItems.add(in_tax)
                        line.save()
        ic_invoice.taxableitem = taxableitem
        for k,v in tax_types.items() :
            a =TaxTotals(taxType = k , amount = v , parent_id = ic_invoice.id , parent_type = "EInvoice" )
            a.save()
            ic_invoice.taxTotals.add(a)
            ic_invoice.save()
        response = post_to_auth_upload(ic_invoice.id)
        try:
            my_json= json.loads(response.get("message")[2:len(response.get("message")) -1])
            ic_invoice.submissionId = my_json.get("submissionId") if my_json else None
        except:
            pass
        ic_invoice.message_Serv = response
        ic_invoice.save()




        return ({"creates":"created"})

############## create invoice fom erpnext ####################
from payer.models import PayerAccount
def create_e_invoice(data):
    invoice = data

    ic_invoice = EInvoice()
    # issuer = invoice.get('issuer')
    # ic_invoice.uploader_id = str(invoice.get('uploader_id'))
    issuer = PayerAccount.objects.all().first()
    print("issuerrr",issuer)
    ic_invoice.issuer_type = issuer.issuer_type
    ic_invoice.issuer_id = issuer.issuer_id
    ic_invoice.issuer_name = issuer.issuer_name
    # address = issuer.get('address')
    ic_invoice.issuer_address_branchId =issuer.issuer_address_branchId
    ic_invoice.issuer_address_country = issuer.issuer_address_country
    ic_invoice.issuer_address_governate = issuer.issuer_address_governate
    ic_invoice.issuer_address_regionCity = issuer.issuer_address_regionCity
    ic_invoice.issuer_address_street = issuer.issuer_address_street
    ic_invoice.issuer_address_buildingNumber = issuer.issuer_address_buildingNumber
    ic_invoice.receiver_type = invoice.get('receiver_type')
    ic_invoice.receiver_id = str(invoice.get('receiverid')).split('.')[0]
    ic_invoice.receiver_name = invoice.get('receivername') or ''
    # receiver_address                           = invoice.get('receiver_address')
    ic_invoice.receiver_address_branchId = str(invoice.get('branchid')).split('.')[0]
    ic_invoice.receiver_address_country = invoice.get('country_code')
    ic_invoice.receiver_address_governate = invoice.get('governate')
    ic_invoice.receiver_address_regionCity = invoice.get('regioncity')
    ic_invoice.receiver_address_street = invoice.get('street')
    ic_invoice.receiver_address_buildingNumber = str(invoice.get('buildingnumber')).split('.')[0]

    # set document info
    ic_invoice.datetimestr = invoice.get('datetime_issued')
    ic_invoice.dateTimeIssued=invoice.get('datetime_issued')
    ic_invoice.documentType = invoice.get('document_type')
    ic_invoice.documentTypeVersion = str(issuer.documentTypeVersion)
    ic_invoice.taxpayerActivityCode = issuer.activty_number
    ic_invoice.internalId = str(invoice.get('internalid')).split('.')[0]
    ic_invoice.save()
    # set Invoice Items
    invoiceLines =invoice.get('items') #json.loads()
    for line in invoiceLines:
        taxes = line.get('item_tax_template')
        # # taxes_list = [{tax.}]
        print("line.get('item_tax_template')",line.get('item_tax_template'))
        print("taxes",taxes)
        tax_cat = TaXCategory.objects.filter(name=taxes).first()
        print("taxxxxx",tax_cat)
        if not tax_cat:
            print("asssssssssss")
            pass
            # return {'error': "Not valid tax catigory"}
        # unitValue = line.get('unitValue')
        ic_invoice.invoiceLines.create(

            description=line.get('description'),
            itemType=line.get('item_type'),
            itemCode=line.get('item_code'),
            unitType=line.get('uom'),
            quantity=float(line.get('qty')),
            unitValue_currencySold='EGP',
            unitValue_amountEGP=round(float(line.get('rate') or 0), 4),
            parent_type="EInvoice",
            parent_id=ic_invoice.id,
            tax_cat=tax_cat,
            discount_amount=float(line.get('discount_amount'))

        )
        ic_invoice.save()
    tax_types = {}
    for line in ic_invoice.invoiceLines.all():

        for tax in line.tax_cat.tax_table.all():
            rate = tax.rate
            amount = tax.amount
            if tax.rate and tax.rate > 0:
                amount = ((float(rate) / 100) * (float(line.unitValue_amountEGP or 0))) - float(
                    line.discount_amount or 0)

            amount = amount * float(line.quantity or 0)
            print(amount)
            in_tax = taxableItems(taxType=tax.taxType, rate=tax.rate,
                                  subType=tax.subType, amount=round(amount, 4), parent_id=line.id,
                                  parent_type='invoiceLines')
            for k, v in tax_types.items():
                if k == tax.taxType:
                    tax_types[k] = float(v) + float(amount)
            if tax.taxType not in tax_types.keys():
                tax_types[tax.taxType] = float(amount)

            in_tax.save()
            line.taxableItems.add(in_tax)
            line.save()
    for k, v in tax_types.items():
        a = TaxTotals(taxType=k, amount=v, parent_id=ic_invoice.id, parent_type="EInvoice")
        a.save()
        ic_invoice.taxTotals.add(a)
        ic_invoice.save()
  
    response = post_to_auth_upload(ic_invoice.id)
    ic_invoice.message_Serv = response
    ic_invoice.save()

    return ({"creates": "created"})
