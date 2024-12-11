


def get_json_object():
    json_object = {
    "header" :{
        "dateTimeIssued"    :"" ,
        "receiptNumber"     :"" ,
        "uuid"              :"" ,
        # "referenceUUID" : "",
        "previousUUID"      :"" ,
        "referenceOldUUID"     :"",
        "currency"          :"",
        # "exchangeRate"      : 0,
        "sOrderNameCode"    :"",
        "orderdeliveryMode" :"" ,
        "grossWeight"       :0 ,
        "netWeight"         :0   
                } ,

    "documentType" : {
        "receiptType" :"s" ,
        "typeVersion" :"1.2"
    } ,
    "seller" :{
        "rin"                :"" ,
        "companyTradeName"   :"" ,
        "branchCode"         :"" ,
        "branchAddress"      : {
                                "country"        :"EG" , 
                                "governate"      :"" ,
                                "regionCity"     :"" ,
                                "street"         :"",  
                                "buildingNumber" :"",
                           
                               } ,
        "deviceSerialNumber" :"" ,
        "activityCode"       :""
    },
    "buyer" :{
        "type"         :"" ,
        "id"           :"" ,
        "name"         :"" ,
        "mobileNumber" :"",
        "paymentNumber":""
    } ,
    "itemData" : [
        {
            "internalCode" :"" ,
            "description" :"" ,
            "itemType" :"" ,
            "itemCode" :"" ,
            "unitType" :"" ,
            "quantity":0 ,
            "unitPrice" : 0 ,
            "netSale" :0 ,
            "totalSale" : 0 ,
            "total" : 0 ,
            "commercialDiscountData" :[
                { "amount" : 0 ,
                 "description" : ""
                 
                }
            ],
            "itemDiscountData" :[
                { "amount" : 0 ,
                 "description" : ""
                 
                }
            ],
            "valueDifference" :0 ,
            "taxableItems" :[
                {
                    "taxType" :"" ,
                    "amount" : 0 , 
                    "subType" : "" ,
                    "rate" : 0
                }
            ]

        }

                ] ,
    "totalSales" : 0 ,
    "totalCommercialDiscount" : 0 ,
    "totalItemsDiscount" : 0 , 
    "extraReceiptDiscountData" : [
                { "amount" : 0 ,
                 "description" : ""
                 }
                 ] ,
    
    "netAmount" :0 ,
    "feesAmount" : 0 ,
    "totalAmount" : 0 ,
    "taxTotals" :[
        {"taxType" : "" ,
        "amount" : 0}

                 ] ,

    "paymentMethod" :"C" ,
    "adjustment" : 0 ,



    }

    return json_object