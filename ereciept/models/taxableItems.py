from django.db import models
from rest_framework import serializers
from .TaxTypes import TaxTypes , TaxSubtypes



class taxableItems(models.Model):
    """
    REF TODO 5-14 taxableItems
    
    """
    taxType = models.ForeignKey(TaxTypes ,on_delete=models.DO_NOTHING, null=True ,blank= True)
    amount  = models.FloatField(max_length=10 , null= True ,blank=True)
    subType = models.ForeignKey( TaxSubtypes,on_delete=models.DO_NOTHING, null=True ,blank= True)
    rate    = models.FloatField(max_length=10 , null= True ,blank=True)


class taxTotals(models.Model) :
    """ 
    REF TODO 
    13 - taxTotals 
    """
    taxType = models.CharField(max_length=80 , null=True ,blank= True)
    amount  = models.FloatField(max_length=10 , null= True ,blank=True)


class TaxTemplate(models.Model):
    name = models.CharField(max_length=80 ,unique=True)
    taxes = models.ManyToManyField(taxableItems)

    def __str__(self):
        return str(self.name) if self.name else str(self.id)