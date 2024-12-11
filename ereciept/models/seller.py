from django.db import models
from .masterData import CountryCode



ENVIROMENT = [("production" , "production" ) , ("preproduction" , "preproduction" )]
class Seller(models.Model) :
    rin                    = models.CharField(max_length=80 )
    companyTradeName       = models.CharField(max_length=80 )
    branchCode             = models.CharField(max_length=80 , null= True ,blank=True ,default=0)
    #  3-4 branchAddress --object 
    country                = models.CharField(max_length=80 , null= True ,blank=True)
    governate              = models.CharField(max_length=80 , null= True ,blank=True)
    regionCity             = models.CharField(max_length=80 , null= True ,blank=True)
    street                 = models.CharField(max_length=80 , null= True ,blank=True)
    buildingNumber         = models.CharField(max_length=80 , null= True ,blank=True)
    postalCode             = models.CharField(max_length=80 , null= True ,blank=True)
    floor                  = models.CharField(max_length=80 , null= True ,blank=True)
    room                   = models.CharField(max_length=80 , null= True ,blank=True)
    landmark               = models.CharField(max_length=80 , null= True ,blank=True)
    additionalInformation  = models.CharField(max_length=80 , null= True ,blank=True)
    deviceSerialNumber     = models.CharField(max_length=80 , null= True ,blank=True)
    pososversion           = models.CharField(max_length=80 , null= True ,blank=True)
    syndicateLicenseNumber = models.CharField(max_length=80 , null= True ,blank=True)
    activityCode           = models.CharField(max_length=80 , null= True ,blank=True)

    current_s  = models.BooleanField(default=1)
    api_key    = models.CharField(max_length=80 , null= True ,blank=True)
    api_secret =  models.CharField(max_length=80 , null= True ,blank=True)
    enviroment = models.CharField(max_length=80 , null =True , blank=True  ,choices=ENVIROMENT ,default="preproduction")

    def __str__(self):
        return self.companyTradeName or str(self.id)