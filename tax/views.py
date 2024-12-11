import json
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import TaXCategory , taxableItems
from home.models import TAXES_CODES , TAX_SUBTYPE  ,TaxableTypes , TaxSubtypes
from django.db.models import Q
@login_required(login_url='login')
def taxes_list(request):
    taxes = TaXCategory.objects.all()
    page = "taxes_list.html"
    content = {
        'taxes' : taxes
    }
    return render(request , page, content)


@login_required(login_url='login')
def taxestype_list(request):
    q= ''
    taxes = TaxableTypes.objects.all()
    if request.GET.get("q"):
        q = request.GET.get("q")
        taxes = TaxableTypes.objects.filter(Q(Code__icontains= q) |
        Q(Desc_en__icontains= q) | Q(Desc_ar__icontains= q) )
    page = "taxes_types.html"
    content = {
        'taxes' : taxes ,
        'q' : q
    }
    return render(request , page, content)


@login_required(login_url='login')
def taxessubtype_list(request):
    q= ''
    taxes = TaxSubtypes.objects.all()
    if request.GET.get("q"):
        q = request.GET.get("q")
        taxes = TaxSubtypes.objects.filter(Q(Code__icontains= q) |
        Q(Desc_en__icontains= q) | Q(Desc_ar__icontains= q) )
    page = "taxes_types.html"
    content = {
        'taxes' : taxes ,
        'q' : q
    }
    return render(request , page, content)


@login_required(login_url='login')
def creat_tax (request) :
    if request.method=='POST' :
        tax= TaXCategory(
            name = request.POST.get('tax_name'),
            validFrom = request.POST.get('validfrom'),
            validTo = request.POST.get('validto')
        )
        tax.save()
        return redirect ('tax_details' , tax.id)


def delete_tax(request , id ):
    TaXCategory.objects.get(id=id ).delete()
    return redirect('taxes_list')



def get_available_subtype(request):
    print("GET",request)
    if request.GET.get('taxType'):
        taxe_types = TaxSubtypes.objects.filter(TaxtypeReference =request.GET.get('taxType') )
        lst =[ {"Code" : i.Code , "Desc_en" :i.Desc_ar} for i in taxe_types ]
        return JsonResponse( {"data":lst })
    else: 
        return JsonResponse({"data" :[] })
@login_required(login_url='login')
def tax_details(request , id ):
    tax= TaXCategory.objects.filter(id = id).first()
    page = 'tax_details.html'
    # taxe_codes = [{'val' : i[0] , 'text' : i[1] } 
    #             for i in TAXES_CODES]
    # taxe_types = [{'val' : i[0] , 'text' : i[1] } 
    #             for i in TAX_SUBTYPE ]


    taxe_codes = TaxableTypes.objects.all()
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
            taxType = request.POST.get('taxType') ,
            amount = float (request.POST.get('amount') or 0 ),
            subType = request.POST.get('suptype') ,
            rate = float (request.POST.get('rate') or 0 ),
            parent_id= tax.id

        )
        taxe_table.save()
        tax.tax_table.add(taxe_table)
        tax.save()
        return redirect('tax_details' , tax.id)

        
               
    return render (request ,page , content)


def delete_taxable_item(request , id):
    item = taxableItems.objects.get(id=id)
    tax_id = item.parent_id
    item.delete()
    return redirect ('tax_details' , tax_id)
