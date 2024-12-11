from hashlib import sha256
from django.db import models

from ereciept.utils import serialize
from .masterData import currency_choises , deliveryModeChoices ,PayerTypeChoices ,paymentMethodChoices
from .seller import Seller
from .itemData import itemData
from .discountmodel import DiscountObj
from .taxableItems import taxTotals  ,TaxTemplate
from datetime import datetime
from django.urls import reverse

class ReceieptSerial(models.Model):
    serial =  models.CharField(max_length=80 , null=True ,blank= True ,default="SAL-INV-")
    name   =  models.CharField(max_length=80 , null=True ,blank= True)
    def save(self , *args , **kwargs) :
        if self.id :
             self.name = f"{str(self.serial)}{str(self.id)} "
        return super(ReceieptSerial, self).save(*args, **kwargs)
    def __str__(self) :
        return self.name if self.name else f"{str(self.serial)}{str(self.id)} "


class NewReceieptSerial(models.Model):
    serial =  models.CharField(max_length=80 , null=True ,blank= True ,default="NEW-INV-")
    name   =  models.CharField(max_length=80 , null=True ,blank= True)
    def save(self , *args , **kwargs) :
        if self.id :
             self.name = f"{str(self.serial)}{str(self.id)} "
        return super(NewReceieptSerial, self).save(*args, **kwargs)
    def __str__(self) :
        return self.name if self.name else f"{str(self.serial)}{str(self.id)} "
class Receiept(models.Model):
    #header 1 
    """ 
    REF TODO header Point 1

    """
    #django related Fields 
    created_at        = models.DateTimeField(auto_now_add=True ,blank=True ,null=True)
    updated_at        = models.DateTimeField(blank=True , null= True)
    #invocie realating fileds 
    postingdate       = models.DateTimeField (null= True , blank=True)
    #  Mandatory, DateTime in UTC, example 2022-02-03T00:00:00Z
    dateTimeIssued    = models.CharField(max_length=80 , null=True ,blank= True) # 1-1
    receiptNumber     = models.CharField(max_length=80 , null=True ,blank= True) # 1-2
    uuid              = models.CharField(max_length=80 , null=True ,blank= True) # 1-3
    previousUUID      = models.CharField(max_length=80 , null=True ,blank= True) # 1-4
    referenceOldUUID  = models.CharField(max_length=80 , null=True ,blank= True) # 1-5
    currency          = models.CharField(max_length=80 , null=True ,blank= True ,choices=currency_choises ,
                                                                                 default="EGP") #1-6
    exchangeRate      = models.FloatField(max_length=10 , null= True ,blank=True ,default=1) # 1-7
    sOrderNameCode    = models.CharField(max_length=80 , null=True ,blank= True)  # 1-8 
    orderdeliveryMode = models.CharField(max_length=80 , null=True ,blank= True ,choices=deliveryModeChoices  ,
                                                                                  default="FC") # 1-9
    grossWeight       = models.FloatField(max_length=10 , null= True ,blank=True) # 1-10
    netWeight         = models.FloatField(max_length=10 , null= True ,blank=True) # 1-11

    #2 2- documentType --object 

    receiptType = models.CharField(max_length=80 , null=True ,blank= True ,default="s")
    typeVersion = models.CharField(max_length=80 , null=True ,blank= True ,default="1.2")
    is_return   = models.BooleanField(default=False)
    #3 - seller --object
    seller = models.ForeignKey(Seller ,on_delete=models.DO_NOTHING, null=True , blank=True)

    #4- buyer 
    buyer_type          = models.CharField(max_length=80 , null=True ,blank= True ,default="P" ,choices=PayerTypeChoices)
    buyer_id            = models.CharField(max_length=80 , null=True ,blank= True)
    buyer_name          = models.CharField(max_length=80 , null=True ,blank= True)
    buyer_mobileNumber  = models.CharField(max_length=80 , null=True ,blank= True)
    buyer_paymentNumber = models.CharField(max_length=80 , null=True ,blank= True)

    #5- itemData 
    itemData = models.ManyToManyField(itemData ,null= True , blank=True)

    #6- totalSales Mandatory, sum of all sales total elements of receipt lines
    totalSales               = models.FloatField(max_length=10 , null= True ,blank=True ,default=0)
    #7 - totalCommercialDiscount Optional, sum of all discount amount elements of receipts lines
    totalCommercialDiscount  = models.FloatField(max_length=10 , null= True ,blank=True ,default=0)
    #8- totalItemsDiscount Optional, sum of all itemsDiscountAmount elements of receipt lines
    totalItemsDiscount       = models.FloatField(max_length=10 , null= True ,blank=True ,default=0)
    #9- extraReceiptDiscountData --list of objects   --done models.discountmodel.DiscountObj
    extraReceiptDiscountData = models.ManyToManyField(DiscountObj ,null= True , blank=True)
    #10- netAmount Mandatory, Sum of all receipt lines netTotal
    netAmount                = models.FloatField(max_length=10 , null= True ,blank=True ,default=0)
    #11- feesAmount Optional, Is the additional fees amount that will be added to the total of the receipt. This field accepts only zero values
    feesAmount               = models.FloatField(max_length=10 , null= True ,blank=True ,default=0)
    #12 - totalAmount  Mandatory, totalAmount = sum of all receipt line total – total extraDiscountAmount
    totalAmount              =  models.FloatField(max_length=10 , null= True ,blank=True ,default=0)
    #13 - taxTotals --list of objects 
    taxTotals                = models.ManyToManyField(taxTotals,null= True , blank=True)
    #14 -paymentMethod String 
    paymentMethod            =  models.CharField(max_length=80 , null=True ,blank= True)
    #15 -adjustment Optional, monetary amount that will be added to the total of the receipt to perform final adjustments to the total amount of the receipt. This field accepts only zero values. 
    adjustment               = models.FloatField(max_length=10 , null= True ,blank=True ,default=0)


    #local Setting 
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(null= True , blank=True)
    serial_number = models.ForeignKey(ReceieptSerial,on_delete=models.DO_NOTHING, null=True ,blank= True)
    # status = [-1 presaved doc , 0 saved doc , 1 posted doc ]
    docstatus     = models.CharField(max_length=80 , null=True ,blank= True ,default="-1")
    slug         = models.SlugField(max_length=50 , null = True , blank=True)

    status      = models.CharField(max_length=80 , null=True ,blank= True)
    submitionid =  models.CharField(max_length=80 , null=True ,blank= True)
    t_uid       =  models.CharField(max_length=80 , null=True ,blank= True)
    def set_totalSales(self):
        totalSales = 0 
        netAmount = 0 
        totalAmount = 0 
        total_discount = 0 
        com_discount = 0 
        for item in self.itemData.all():
            totalSales = totalSales + float(item.totalSale or 0  )
            netAmount = netAmount + float(item.netSale or 0)
            totalAmount = totalAmount + float(item.total or 0)
            for discount in item.itemDiscountData.all() :
                 total_discount =  total_discount + float(discount.amount or  0)
            for discount_c in item.commercialDiscountData.all() :
                 com_discount =  com_discount + float(discount_c.amount or  0)

        self.totalCommercialDiscount = com_discount
        self.totalItemsDiscount = total_discount
        self.totalSales = totalSales
        self.netAmount = netAmount
        self.totalAmount = totalAmount
    def set_slug(self) :
        new_slug =NewReceieptSerial()
        new_slug.save()
        new_slug.save()
        self.slug = new_slug.id
    #add naming series 
    def set_serial(self) :
        new_serial = ReceieptSerial()
        new_serial.save()
        new_serial.save()
        self.serial_number = new_serial

    #set las update date 
    def set_last_update(self):
        self.updated_at = datetime.now()

    #Create date in iso formate like 2022-02-03T00:00:00Z
    def set_date_iso_formate(self):
        if self.postingdate and not self.dateTimeIssued:
           dateTimeIssued = self.postingdate.isoformat()
           self.dateTimeIssued = str(dateTimeIssued).split('+')[0][0:-2]+"00Z"
    def save(self, *args ,**kwargs):
        if self.buyer_id :
            self.buyer_id = str(self.buyer_id).split('.')[0]
        if not self.slug  :
            self.set_slug()
        if not self.serial_number and self.docstatus =='0':
             self.set_serial()
             self.slug = str(self.serial_number)
           
        self.set_date_iso_formate()
        self.set_last_update()
        if self.id :
             self.set_totalSales()

        if self.is_return  :
            self.receiptType ='r'
        return super(Receiept ,self).save(*args ,**kwargs)
    def get_absolute_url(self):
        return reverse("get_reciept", kwargs={"pk": self.id})
    def __str__(self) :
        return str(self.serial_number) if self.serial_number else str(self.slug)
    
    def set_invoice_uuid(self,serializer_data):
        serialized_invoice = serialize(data=serializer_data)
        self.uuid = sha256(serialized_invoice.encode('utf-8')).hexdigest()



