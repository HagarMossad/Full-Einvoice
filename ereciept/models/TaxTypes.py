from django.db import models

class TaxTypes(models.Model) :
    Code    = models.CharField(max_length=80 , null=True ,blank= True)
    Desc_en = models.CharField(max_length=80 , null=True ,blank= True)
    Desc_ar = models.CharField(max_length=80 , null=True ,blank= True)

    def __str__(self):
        return self.Code

class TaxSubtypes(models.Model) :
    Code            = models.CharField(max_length=80 , null=True ,blank= True)
    Desc_en         = models.CharField(max_length=80 , null=True ,blank= True)
    Desc_ar         = models.CharField(max_length=80 , null=True ,blank= True) 
    TaxtypeReference= models.ForeignKey(TaxTypes,on_delete=models.DO_NOTHING , null=True ,blank= True) 
    def __str__(self):
        return self.Code