from django.db import models

# import related tables 
from .taxableItems import taxableItems ,TaxTemplate
from .discountmodel import DiscountObj
from .masterData import itemTypeChoisec ,unitTypeChoices


class itemData(models.Model) :
    """
    ref 5- itemData
    
    """
    internalCode           = models.CharField(max_length=80 , null=True , blank=True)
    description            = models.CharField(max_length=80 , null=True , blank=True)
    itemType               = models.CharField(max_length=80 , null=True , blank=True ,choices=itemTypeChoisec)
    itemCode               = models.CharField(max_length=80 , null=True , blank=True )
    unitType               = models.CharField(max_length=80 , null=True , blank=True ,choices=unitTypeChoices) 
    quantity               = models.FloatField(max_length=10 , null= True ,blank=True)
    unitPrice              = models.FloatField(max_length=10 , null= True ,blank=True)
    netSale                = models.FloatField(max_length=10 , null= True ,blank=True)
    totalSale              = models.FloatField(max_length=10 , null= True ,blank=True)
    total                  = models.FloatField(max_length=10 , null= True ,blank=True)
    commercialDiscountData = models.ManyToManyField(DiscountObj ,null=True , blank=True)
    itemDiscountData       = models.ManyToManyField(DiscountObj ,related_name="itemdiscout",null=True , blank=True)
    valueDifference        = models.FloatField(max_length=10 , null= True ,blank=True ,default=0)
    taxableItems           = models.ManyToManyField(taxableItems ,null=True , blank=True)


    #django required 
    parent = models.CharField(max_length=80 , null=True , blank=True)

    #add template to line 
    taxtemplate = models.ForeignKey(TaxTemplate , blank=True ,null=True,on_delete=models.DO_NOTHING)
    rd_tax      = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)


    # this method to caculate tax amount 
   
    def caculate_tax_item(self):
        # tow deffrent methods 
        #taxes fees / non taxes fees 
        self.taxableItems.clear()
        tax_amount = 0
        taxes =[]
        if self.taxtemplate :
            template_id =  self.taxtemplate.id 
            tax = TaxTemplate.objects.filter(id=template_id).first()   
            for tax_line in tax.taxes.all() :
                taxes.append(tax_line.id)
            
            for tax_id in taxes :
                line_tax_amount = 0 
                tax_item = taxableItems.objects.get(id =tax_id)
                #calculate tax amount and line tax amount 

                if float(tax_item.amount or 0 ) > 0  :
                    line_tax_amount = float(tax_item.amount or 0 ) * float(self.quantity or 0) 
                
                if (float(tax_item.amount or 0 ) == 0)  and  (float(tax_item.rate or 0) ==0 ) :
                     line_tax_amount = float(self.rd_tax or 0 ) * float(self.quantity or 0) 
                if (float(tax_item.amount or 0 ) == 0)    and  (float(tax_item.rate or 0) > 0 ):
                    #caculate rate
                    line_tax_amount = ((float(tax_item.rate or 0) / 100) * (float(self.unitPrice or 0) -float(self.get_total_discount() ) ))* float(self.quantity or 0)
              
                t = taxableItems(
                    taxType =  tax_item.taxType ,
                    amount = line_tax_amount  ,
                    subType =  tax_item.subType ,
                    rate =  tax_item.rate
                )
                t.save()
                self.taxableItems.add(t.id)
                tax_amount = tax_amount + line_tax_amount 
        
              
        return tax_amount    

     
    def get_total_discount(self) :
        # 2 discount tables  commercialDiscountData , itemDiscountData discount set in invoice currency 
        commercialDiscountData  = 0 
        itemDiscountData = 0 
        for codc in self.commercialDiscountData.all() :
            commercialDiscountData += float(codc.amount or 0)
        # for itdc in self.itemDiscountData.all() :
        #      itemDiscountData += float(itdc.amount or 0)
        return  commercialDiscountData
    def get_currency_factor(self):
        # need to update to fetch the currency rate from parent doc 
        # now it jsut return 1 for EGP 
        return 1
   

    def get_totalSale(self) :
        factor = float(self.get_currency_factor() or 1)
        self.totalSale = float(self.quantity or 1 )*( float(self.unitPrice or 1) * factor)
        self.netSale =  self.totalSale -self.get_total_discount()

    def get_total (self) :
        self.total = ( self.totalSale+ float (self.caculate_tax_item()) or 0 )- self.get_total_discount()
        
    #methods --on save caculate netSale totalSale total , commercialDiscountData , itemDiscountData
    def set_total_fields (self) :
      
        self.get_totalSale()



    def save(self, *args,**kwargs):
        if self.id :
             self.set_total_fields()
             self.caculate_tax_item()
             self.get_total()
        return super(itemData,self ).save(*args,**kwargs)

    