
from ereciept.models.taxableItems import taxTotals, taxableItems
from ereciept.models.discountmodel import DiscountObj
from ereciept.models.ereciept import Receiept
# from ereciept.models.header import Header
from ereciept.models.seller import Seller
from ereciept.models.itemData import itemData

from rest_framework import serializers , exceptions





class headerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiept
        fields = (
            'dateTimeIssued',
            'receiptNumber',
            'uuid',
            'previousUUID',
            'referenceOldUUID',
            'currency',
            'exchangeRate',
            'sOrderNameCode',
            'orderdeliveryMode',
            'grossWeight',
            'netWeight'

        )


class headerWithoutUUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiept
        fields = (
            'dateTimeIssued',
            'receiptNumber',
            'uuid',
            'previousUUID',
            'referenceOldUUID',
            'currency',
            'exchangeRate',
            'sOrderNameCode',
            'orderdeliveryMode',
            'grossWeight',
            'netWeight'

        )



class documentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiept
        fields = (
            'receiptType',
            'typeVersion',
        )






class branchAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            'country',
            'governate',
            'regionCity',
            'street',
            'buildingNumber',
            'postalCode',
            'floor',
            'room',
            'landmark',
            'additionalInformation',
        )

class sellerSerializer(serializers.ModelSerializer):
    branchAddress = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Seller
        fields = (
            'rin',
            'companyTradeName',
            'branchCode',
            'branchAddress',
            'deviceSerialNumber',
            'syndicateLicenseNumber',
            'activityCode'
        )

    def get_branchAddress(self,obj):
        print("get_branchAddress ============> " , obj)
        return branchAddressSerializer(obj).data




class buyerSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="buyer_type")
    id = serializers.CharField(source="buyer_id")
    name = serializers.CharField(source="buyer_name")
    mobileNumber = serializers.CharField(source="buyer_mobileNumber")
    paymentNumber = serializers.CharField(source="buyer_paymentNumber")
    class Meta:
        model = Receiept
        fields = (
            'type',
            'id',
            'name',
            'mobileNumber',
            'paymentNumber',
        )





class discountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountObj
        fields = (
            'amount',
            'description',
        )

class taxTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = taxTotals
        fields = (
            'taxType',
            'amount',
        )

class taxableItemsSerializer(serializers.ModelSerializer):
    taxType = serializers.CharField(read_only=True,source="taxType.Code")
    subType = serializers.CharField(read_only=True,source="subType.Code")
    class Meta:
        model = taxableItems
        fields = (
            'taxType',
            'amount',
            'subType',
            'rate',
        )

class itemDataSerializer(serializers.ModelSerializer):
    commercialDiscountData = discountSerializer(many=True)
    itemDiscountData = discountSerializer(many=True)
    taxableItems = taxableItemsSerializer(many=True)
    class Meta:
        model = itemData
        fields = (
            'internalCode',
            'description',
            'itemType',
            'itemCode',
            'unitType',
            'quantity',
            'unitPrice',
            'netSale',
            'totalSale',
            'total',
            'commercialDiscountData',
            'itemDiscountData',
            'valueDifference',
            'taxableItems',
        )







class ReceieptSerializer(serializers.ModelSerializer):
    header = serializers.SerializerMethodField(read_only=True)
    documentType = serializers.SerializerMethodField(read_only=True)
    seller = serializers.SerializerMethodField(read_only=True)
    buyer = serializers.SerializerMethodField(read_only=True)
    itemData = itemDataSerializer(many=True)
    taxTotals = taxTotalSerializer(many=True)
    extraReceiptDiscountData = discountSerializer(many=True)

    class Meta:
        model = Receiept
        fields = (
            'header',
            'documentType',
            'seller',
            'buyer',
            'itemData',
            'totalSales',
            'totalCommercialDiscount',
            'totalItemsDiscount',
            'extraReceiptDiscountData',
            'netAmount',
            'feesAmount',
            'totalAmount',
            'taxTotals',
            'paymentMethod',
            'adjustment',
            # 'contractor',
            # 'beneficiary'
            
        )

    def get_header(self,obj) :
        #print ("obj ======> ", obj)
        return headerSerializer(obj).data
    def get_documentType(self,obj):
        return documentSerializer(obj).data
    def get_buyer(self,obj):
        return buyerSerializer(obj).data

    def get_seller(self,obj):
        return sellerSerializer(obj.seller).data


class ReceieptWithoutUUIDSerializer(serializers.ModelSerializer):
    header = serializers.SerializerMethodField(read_only=True)
    documentType = serializers.SerializerMethodField(read_only=True)
    seller = serializers.SerializerMethodField(read_only=True)
    buyer = serializers.SerializerMethodField(read_only=True)
    itemData = itemDataSerializer(many=True)
    taxTotals = taxTotalSerializer(many=True)
    extraReceiptDiscountData = discountSerializer(many=True)

    class Meta:
        model = Receiept
        fields = (
            'header',
            'documentType',
            'seller',
            'buyer',
            'itemData',
            'totalSales',
            'totalCommercialDiscount',
            'totalItemsDiscount',
            'extraReceiptDiscountData',
            'netAmount',
            'feesAmount',
            'totalAmount',
            'taxTotals',
            'paymentMethod',
            'adjustment',
            # 'contractor',
            # 'beneficiary'
            
        )

    def get_header(self,obj) :
        #print ("obj ======> ", obj)
        return headerWithoutUUIDSerializer(obj).data
    def get_documentType(self,obj):
        return documentSerializer(obj).data
    def get_buyer(self,obj):
        return buyerSerializer(obj).data

    def get_seller(self,obj):
        return sellerSerializer(obj.seller).data




    # def get_Order_Delivery_Status(self,obj):
    #     # print ("obj ======> ", obj.Order_Delivery_Status)
    #     return order_delivery_status.get(obj.Order_Delivery_Status or 1)
