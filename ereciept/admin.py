from django.contrib import admin
from .models.header import Header
from .models.discountmodel import DiscountObj
from .models.taxableItems import taxableItems  ,TaxTemplate
from.models.TaxTypes import TaxTypes ,TaxSubtypes
from .models.ereciept import ReceieptSerial ,Receiept
from .models.itemData import itemData 
from  .models.seller import Seller
from .models.uplload_sheet import Sheet
# Register your models here.
admin.site.register(ReceieptSerial)
admin.site.register(TaxTypes )
admin.site.register(TaxSubtypes )
admin.site.register(Receiept)
admin.site.register(itemData)
admin.site.register(taxableItems)
admin.site.register(TaxTemplate)
admin.site.register(Seller)
admin.site.register(Sheet)
admin.site.register(DiscountObj)