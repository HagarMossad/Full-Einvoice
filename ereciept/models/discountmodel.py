from django.db import models

class DiscountObj(models.Model):
    """
        ToDO ref 5-11 commercialDiscountData , 5-12  itemDiscountData
    """
    amount      = models.FloatField(max_length=10 , null= True ,blank=True) # 5-11-1 ,5-12-1
    description = models.CharField(max_length=80 , null=True ,blank= True) #  5-11-2 ,5-12-2
