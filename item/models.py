from django.db import models
from home.models import UOM 
# Create your models here.
class Item (models.Model):
    description = models.CharField(max_length=250, null=True , blank=True)
    itemType = models.CharField(max_length=250,null=True , blank=True)
    itemCode =  models.CharField(max_length=250 ,null=True , blank=True)
    unitType = models.CharField(max_length=250 , choices=UOM ,null=True , blank=True)
    internalCode =  models.CharField(max_length=250 , null=True , blank=True)
    unitValue_currencySold =  models.CharField(max_length=250, default='EGP')
    unitValue_amountEGP = models.DecimalField(decimal_places=5 , max_digits=100 ,null=True , blank=True)