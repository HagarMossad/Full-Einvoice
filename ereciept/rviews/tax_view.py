from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from ereciept.models.taxableItems import *
from ereciept.models.TaxTypes import TaxSubtypes , TaxTypes



@login_required(login_url='login')
def tax_list(request):
    taxes = TaxTemplate.objects.all()
    page = "pages/taxe_list.html"
    content = {
        "taxes" : taxes
    }
    return render(request ,page ,content) 




@login_required(login_url='login')
def creat_tax (request) :
    if request.method=='POST' :
        tax= TaxTemplate(
            name = request.POST.get('tax_name'),
            # validFrom = request.POST.get('validfrom'),
            # validTo = request.POST.get('validto')
        )
        tax.save()
        return redirect ('reciept_tax_details' , tax.id)


@login_required(login_url='login')
def tax_details(request , id ):
    tax= TaxTemplate.objects.filter(id = id).first()
    page = 'pages/tax_details.html'
    taxe_codes =TaxTypes.objects.all()
    taxe_types = TaxSubtypes.objects.all()
    if request.GET.get('taxtype'):
        taxe_types = TaxSubtypes.objects.filter(TaxtypeReference =request.GET.get('taxtype') )

    content = {
        'tax' :tax,
        'taxe_codes' : taxe_codes ,
        'taxe_types' : taxe_types 
        
    }

    if request.method == 'POST' :
        taxe_table = taxableItems(
            taxType = TaxTypes.objects.get(Code = request.POST.get('taxType') ),
            amount = float (request.POST.get('amount') or 0 ),
            subType = TaxSubtypes.objects.get(Code =request.POST.get('suptype')) ,
            rate = float (request.POST.get('rate') or 0 ),
            # parent_id= tax.id

        )
        taxe_table.save()
        tax.taxes.add(taxe_table)
        tax.save()
        return redirect('reciept_tax_details' , tax.id)

        
               
    return render (request ,page , content)


def delete_taxable_item(request , id):
    item = taxableItems.objects.get(id=id)
    tax_id = item.parent_id
    item.delete()
    return redirect ('reciept_tax_details' , tax_id)
