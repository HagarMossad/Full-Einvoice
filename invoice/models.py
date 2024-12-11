from django.db import models

# Create your models here.
from tax.models import taxableItems , TaXCategory , TaxTotals

from home.models import UOM ,AccountType ,COUNTY_CODES , DOCUMENTTYPE ,DocumentTypeVersion , Receiver
from payer.models import PayerAccount

from django.db.models.signals import pre_save ,post_save
from django.db.models import Sum
from django.dispatch import receiver
from item.models import Item

class InoiveFile(models.Model) :

    status = models.CharField(max_length=250 , null=True , blank=True)
    sheet = models.FileField(upload_to = 'uploader')

class  Payment(models.Model):
    bankName        = models.CharField(max_length=250 , null=True , blank=True )
    bankAddress     = models.CharField(max_length= 250 , null= True , blank=True)
    bankAccountNo   = models.CharField(max_length= 250 , null= True , blank=True)
    bankAccountIBAN = models.CharField(max_length= 250 , null= True , blank=True)
    swiftCode       = models.CharField(max_length= 250 , null= True , blank=True)
    terms           =  models.CharField(max_length= 250 , null= True , blank=True)

    def __str__(self):
        return self.bankName


class InvoiceLine(models.Model):
    item = models.ForeignKey(Item , on_delete=models.CASCADE , null=True , blank=True)
    description = models.CharField(max_length=250, null=True , blank=True)
    itemType = models.CharField(max_length=250,null=True , blank=True)
    itemCode =  models.CharField(max_length=250 ,null=True , blank=True)
    unitType = models.CharField(max_length=250 , choices=UOM ,null=True , blank=True)
    quantity = models.DecimalField(decimal_places=2 , max_digits=100)
    unitValue_currencySold =  models.CharField(max_length=250, default='EGP')
    unitValue_amountEGP = models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True)
    unitValue_amountSold = models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True)
    unitValue_currencyExchangeRate =  models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True)
    salesTotal = models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True)
    total = models.DecimalField(decimal_places=5 , max_digits=1100 ,null=True , blank=True)
    valueDifference =models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True , default=0) 
    totalTaxableFees = models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True , default=0)
    netTotal = models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True , default=0)
    itemsDiscount =  models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True , default=0)
    discount_rate =models.DecimalField(decimal_places=5 , max_digits=1000 ,null=True , blank=True , default=0)
    discount_amount=models.DecimalField(decimal_places=5 , max_digits=1000 ,null=True , blank=True , default=0)
    taxableItems = models.ManyToManyField(taxableItems , null=True , blank=True) 
    internalCode =  models.CharField(max_length=250 , null=True , blank=True)
    tax_cat = models.ForeignKey(TaXCategory , null=True , blank=True , on_delete=models.CASCADE)
    item_tax = models.DecimalField(decimal_places=5 , max_digits= 1000 , blank=True , null=True )
    total_taxes_fees =  models.DecimalField(decimal_places=5 , max_digits= 1000 , blank=True , null=True )
    parent_id = models.CharField(max_length=250 , null=True , blank=True)
    parent_type = models.CharField(max_length=250 , null=True , blank=True)
    rd_tax = models.DecimalField(decimal_places=5, max_digits=1000, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.item :
            self.description = self.item.description
            self.itemType    = self.item.itemType
            self.itemCode    = self.item.itemCode
            self.unitType    = self.item.unitType
        total_daiscount  = float(self.discount_amount) * float(self.quantity)
        self.salesTotal = float(self.quantity or 0 )  * float(self.unitValue_amountEGP )
        self.item_tax = 0 
        if self.id :
            for tax in self.taxableItems.all() :
                self.item_tax += round (float(tax.amount or  0 )  , 5)
            self.total_taxes_fees = round ((float(self.quantity) * float(self.item_tax)) , 5)
            self.total = round (((float(self.salesTotal) +  float( self.item_tax or 0 )) - total_daiscount) , 5 )
            self.netTotal = float(self.salesTotal) - float(total_daiscount)
        return super(InvoiceLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class EInvoice (models.Model) :
    #issuer info
    payer_account = models.ForeignKey(PayerAccount , on_delete=models.CASCADE , null=True , blank=True)
    uploader_id  =models.CharField(max_length=250 ,blank=True ,null=True)
    issuer_type =models.CharField(max_length=250,choices=AccountType ,blank=True ,null=True)
    issuer_id=models.CharField(max_length=250 ,blank=True ,null=True)
    issuer_name=models.CharField(max_length=250 ,blank=True ,null=True)
    issuer_address_branchId=models.CharField(max_length=250 ,blank=True ,null=True)
    issuer_address_country=models.CharField(max_length=250, choices=COUNTY_CODES,blank=True ,null=True)
    issuer_address_governate=models.CharField(max_length=250 ,blank=True ,null=True)
    issuer_address_regionCity=models.CharField(max_length=250 ,blank=True ,null=True)
    issuer_address_street=models.CharField(max_length=250 ,blank=True ,null=True)
    issuer_address_buildingNumber=models.CharField(max_length=250  ,blank=True ,null=True)
    #receiver Info
    receiver_account = models.ForeignKey(Receiver , on_delete=models.CASCADE , null=True , blank=True)
    receiver_type =models.CharField(max_length=250 ,choices=AccountType, blank=True , null=True,)
    receiver_id=models.CharField(max_length=250 , blank=True , null=True)
    receiver_name=models.CharField(max_length=250 , blank=True , null=True)
    receiver_address_branchId=models.CharField(max_length=250 , blank=True , null=True)
    receiver_address_country=models.CharField(max_length=250 , choices=COUNTY_CODES,blank=True , null=True)
    receiver_address_governate=models.CharField(max_length=250 , blank=True , null=True)
    receiver_address_regionCity=models.CharField(max_length=250 , blank=True , null=True)
    receiver_address_street=models.CharField(max_length=250 , blank=True , null=True)
    receiver_address_buildingNumber=models.CharField(max_length=250 , blank=True , null=True)


    # end recsiever section 
    documentType = models.CharField(max_length= 250 , choices=DOCUMENTTYPE )
    documentTypeVersion =  models.CharField(max_length= 250 , choices=DocumentTypeVersion)
    dateTimeIssued = models.DateTimeField(auto_now= False ,auto_now_add=False ,blank=True ,null=True)
    taxpayerActivityCode = models.CharField(max_length= 250)
    internalId= models.CharField(max_length= 250)
    purchaseOrderReference = models.CharField(max_length= 250 , null=True , blank=True)
    purchaseOrderDescription = models.CharField(max_length= 250 , null=True , blank=True)
    salesOrderReference = models.CharField(max_length= 250 , null=True , blank=True)
    salesOrderDescription =  models.CharField(max_length= 250 , null=True , blank=True)
    proformaInvoiceNumber = models.CharField(max_length= 50 , null=True , blank=True)
    
    payment = models.ForeignKey(Payment , on_delete=models.CASCADE , null=True , blank=True)
    #adding tax table item 
    taxableitem = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True , blank=True)
    #main Data 
    datetimestr =  models.CharField(max_length= 250 , null=True , blank=True)
    invoiceLines = models.ManyToManyField(InvoiceLine)
    totalSalesAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True , blank=True)
    totalDiscountAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True , blank=True)
    netAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True , blank=True)
    taxTotals = models.ManyToManyField(TaxTotals ,null=True , blank=True)
    extraDiscountAmount =  models.DecimalField(max_digits=100 , decimal_places=5 ,null=True,blank=True)
    totalItemsDiscountAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True,blank=True)
    totalAmount = models.DecimalField(max_digits=100 , decimal_places=5 ,null=True,blank=True)
    submissionId =models.CharField(max_length=500 , blank=True , null=True)
    docstatus =models.CharField(max_length=500 , blank=True , null=True)
    errro_log =models.CharField(max_length=500 , blank=True , null=True)
    created_date = models.DateTimeField(auto_now_add= True , null =True , blank=True)
    message_Serv = models.TextField(null =True , blank =True   )

    def save(self , *args , **kwargs):
        issuer = PayerAccount.objects.all().first()
        self.issuer_address_street = issuer.issuer_address_street
        reviever = Receiver.objects.filter(receiver_id = self.receiver_id).first()
        if reviever: 
            self.receiver_account = reviever
            self.receiver_type = reviever.receiver_type
            self.receiver_name = reviever.receiver_name
            self.receiver_address_branchId = reviever.receiver_address_branchId
            self.receiver_address_country = reviever.receiver_address_country
            self.receiver_address_governate= reviever.receiver_address_governate
            self.receiver_address_regionCity = reviever.receiver_address_regionCity
            self.receiver_address_street = reviever.receiver_address_street
        
        return super(EInvoice, self).save(*args, **kwargs)

@receiver(pre_save ,sender=EInvoice)
def invoice_totals(sender ,instance , **kwargs):
    if not instance.issuer_id :
        issuer = instance.payer_account
        if not issuer :
            return" error"
        instance.issuer_id = str(issuer.issuer_id)
        instance.issuer_type = issuer.issuer_type
        instance.issuer_name = issuer.issuer_name
        instance.issuer_address_branchId = str(issuer.issuer_address_branchId) 
        instance. issuer_address_country = issuer.issuer_address_country
        instance.issuer_address_governate = issuer.issuer_address_governate
        instance.issuer_address_regionCity = issuer.issuer_address_regionCity
        instance.issuer_address_street =issuer.issuer_address_street
        instance.issuer_address_buildingNumber = issuer.issuer_address_buildingNumber
    
    try:
       
        totalSalesAmount = 0
        totalDiscountAmount = 0
        tax_totals= 0 
        
        for line in instance.invoiceLines.all():
            line.save()

            totalSalesAmount += float(line.salesTotal or 0)
            totalDiscountAmount += float(line.discount_amount or 0) *float(line.quantity or 0)
           
        taxes_al = instance.taxTotals.all()
        if taxes_al :
            for i in taxes_al :
                tax_totals += float(i.amount)
                # i.amount = abs(i.amount)


      
        instance.totalDiscountAmount =  round(float(totalDiscountAmount or 0 ) , 5 )
        instance.totalSalesAmount = round(float(totalSalesAmount) , 5)
        instance.netAmount = round ((float(totalSalesAmount or 0 ) -float(totalDiscountAmount or 0)) , 5)
        instance.totalAmount = round((float( instance.netAmount or 0 ) + float(tax_totals or 0 )), 4 )
       
    except:print('not Done')

