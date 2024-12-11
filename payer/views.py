from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from home.models import Receiver ,AccountType
from .models import PayerAccount , versions


@login_required(login_url='login')
def payer_list(request):
    payers = PayerAccount.objects.all()
    page ='payer_list.html'
    content ={
        'payers' : payers
    }
    return render(request , page , content)



@login_required(login_url='login')
def create_payer(request):
    page = 'payer.html'
    types = [{'v' :i[0] , 'n' :i[1] }
                for i in AccountType ]
    content ={
        'types' :types
    }
    if request.method=="POST":
        payer = PayerAccount(
                
                tax_id  = str( request.POST.get('issuer_id') or '') ,
                user_key  = str(request.POST.get('user_key') or '') ,
                token_key =str( request.POST.get('token_key') or '') ,
                issuer_type = str(request.POST.get('issuer_type') or'') ,
                issuer_id = str(request.POST.get('issuer_id') or'') ,
                issuer_name = request.POST.get('issuer_name') ,
                issuer_address_branchId = str(request.POST.get('issuer_address_branchId') or ''),
                issuer_address_country= request.POST.get('issuer_address_country')  ,
                issuer_address_governate = request.POST.get('issuer_address_governate')  ,
                issuer_address_regionCity = request.POST.get('issuer_address_regionCity')  ,
                issuer_address_street =request.POST.get('issuer_address_street') ,
                issuer_address_buildingNumber = str(request.POST.get('issuer_address_buildingNumber') or ''),
                activty_number = str(request.POST.get('activty_code') or '')

        )
        payer.save()
        user_e = User.objects.get( username= request.POST.get('user')) 
        payer.user.add(user_e.id)
        payer.save()
        return redirect('payer_list')
    return render(request , page , content)
def update_payer(request , id )  :
    profile = PayerAccount.objects.get(id=id)
    page = 'payer.html'
    types = [{'v' :i[0] , 'n' :i[1] }
                for i in AccountType ]
    vers = [{'value' : i[0] ,"key" :i[1] } for i in versions]
    content ={
        'types' :types ,
        'profile' :profile,
        "versions" :vers
    }
    if request.method=='POST':
                profile.tax_id  = str( request.POST.get('issuer_id') or '') 
                profile.user_key  = str(request.POST.get('user_key') or '') 
                profile.token_key =str( request.POST.get('token_key') or '') 
                profile.issuer_type = str(request.POST.get('issuer_type') or'') 
                profile.issuer_id = str(request.POST.get('issuer_id') or'') 
                profile.issuer_name = request.POST.get('issuer_name') 
                profile.issuer_address_branchId = str(request.POST.get('issuer_address_branchId') or '')
                profile.issuer_address_country= request.POST.get('issuer_address_country')  
                profile.issuer_address_governate = request.POST.get('issuer_address_governate')  
                profile.issuer_address_regionCity = request.POST.get('issuer_address_regionCity')  
                profile.issuer_address_street =request.POST.get('issuer_address_street') 
                profile.issuer_address_buildingNumber = str(request.POST.get('issuer_address_buildingNumber') or '')
                profile.activty_number = str(request.POST.get('activty_code') or '')
                profile.documentTypeVersion = str(request.POST.get('documentTypeVersion') or '' )
                profile.save()
                return redirect('payer_list')

    return render(request ,page , content)


def delete_payer(request ,id):
    PayerAccount.objects.get(id =id).delete()
    return redirect('payer_list')
