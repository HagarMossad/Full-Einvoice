from django.db import models
import json 
# Create your models here.

# load Currency Data And deliveryMode
# 
from .masterData import currency_choises ,deliveryModeChoices


class Header(models.Model):
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
    exchangeRate      = models.FloatField(max_length=10 , null= True ,blank=True) # 1-7
    sOrderNameCode    = models.CharField(max_length=80 , null=True ,blank= True)  # 1-8 
    orderdeliveryMode = models.CharField(max_length=80 , null=True ,blank= True ,choices=deliveryModeChoices  ,
                                                                                  default="FC") # 1-9
    grossWeight       = models.FloatField(max_length=10 , null= True ,blank=True) # 1-10
    netWeight         = models.FloatField(max_length=10 , null= True ,blank=True) # 1-11
