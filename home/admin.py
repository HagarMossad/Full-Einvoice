from django.contrib import admin
from .models import TaxableTypes , TaxSubtypes ,ReceiverFile ,Receiver ,ErrorLog
# Register your models here.
admin.site.register(TaxSubtypes)
admin.site.register(TaxableTypes)
admin.site.register(ReceiverFile)
admin.site.register(Receiver)
admin.site.register(ErrorLog)