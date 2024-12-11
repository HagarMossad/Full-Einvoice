from django.core.checks import messages
from django.shortcuts import render,redirect
from django.core.paginator import Page, Paginator
# Create your views here.
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Receiver ,AccountType ,TaxableTypes,TaxSubtypes , ReceiverFile ,ErrorLog
# Create your models here.
from pathlib import Path
import json
from django.db.models import Q
BASE_DIR = Path(__file__).resolve().parent.parent
@login_required(login_url='login')
def home (request) :

    tax_path = BASE_DIR / 'e_invoice/TaxTypes.json'
    tax_subtype_path = BASE_DIR / 'e_invoice/TaxSubtypes.json'
    taxtype_json = open(tax_path , encoding= 'utf-8')
    tax_subtype_json = open(tax_subtype_path, encoding= 'utf-8')
    taxtype_data =json.load(taxtype_json)
    tax_subtype_data = json.load(tax_subtype_json)
    init_data = TaxableTypes.objects.all()
    init_sub_data = TaxSubtypes.objects.all()
    if len(init_data) == 0 :
        print("Init Types For first Time ")
        for  i in taxtype_data :
            a = TaxableTypes(
                Code = i.get('Code') , 
                Desc_en= i.get('Desc_en'),
                Desc_ar = i.get("Desc_ar")
            )
            a.save()
    if len(init_sub_data) == 0 :
        print("Init Types For first Time ")
        for  i in tax_subtype_data :
            a = TaxSubtypes(
                Code = i.get('Code') , 
                Desc_en= i.get('Desc_en'),
                Desc_ar = i.get("Desc_ar"),
                TaxtypeReference = i.get('TaxtypeReference')
            )
            a.save()
    page = 'home.html'
    return render (request , page)


def user_login(request) :
    if request.user.is_authenticated  :
        return redirect('home')
    if request.method == 'POST' :
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
             login(request, user)
            
             return JsonResponse({"Message" : "success"  })
        else :
            return JsonResponse({"Message" : "Please Check Your user name or password "})
        
    page = "login.html"
    return render(request , page)


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def user_list(request):
    if not request.user.is_superuser :
        return redirect('home')
    page = 'user_list.html'
    users = User.objects.all()
    content = {
        "users" :users
    }
    return render(request , page , content)

RECIEVR_COL = [
    "Receiver Type" ,
    "Receiver Id" ,
    "Receiver Name" ,
    "Receiver branchID" ,
    "Receiver Country"  , 
    "Receiver Region City" , 
    "Receiver Governate" , 
    "Receiver Street" , 
    "Receiver Building Number"

]
@login_required(login_url='login')
def register_view(request):
    page = "register.html"
    if request.method=="POST" :
        user_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_passsword =request.POST.get('confrim_password')
        if password != confirm_passsword :
            return JsonResponse({'error': 'password dont match'})
        user = User.objects.create_user(user_name, email, password)
        user.is_staff =1
        user.save()
        return JsonResponse({"data" : "created"})
    return render(request , page)
@login_required(login_url='login')
def delete_user(request ,id ):
    User.objects.get(id=id).delete()
    return redirect('user_list')
@login_required(login_url='login')
def update_user(request , id):
    user = User.objects.get(id=id)
    page = "reset_password.html"
    if request.method== "POST":
        if request.POST.get('username') != user.username :
            user.username = request.POST.get('username')
        if request.POST.get("password") :
            user.set_password(request.POST.get("password"))
        user.save()
        return redirect('user_list')

    return render(request , page , {'user':user})
import pandas as pd
def create_import_reciever(  id , pth) :
    data = pd.read_excel( pth  ,sheet_name = 0)
    dat_list = []
    dict_data = {}
    erros = []
    try : 
        for id in range(0 , len(data['Receiver Name'])) :
            items_list = []
            items_data = {}
            try :
                reciver = Receiver(
                    name                            = str(data['Receiver Name'].iloc[id] or  "")  or "",
                    receiver_type                   = str(data['Receiver Type'].iloc[id] or  "")  or "" ,
                    receiver_id                     = str(data['Receiver Id'].iloc[id] or  "")  or "" ,
                    receiver_name                   = str(data['Receiver Name'].iloc[id] or  "")  or "" ,
                    receiver_address_branchId       = str(data['Receiver branchID'].iloc[id] or  "0")  or "0" ,
                    receiver_address_country        = str(data['Receiver Country'].iloc[id] or  "0")  or "0" , 
                    receiver_address_governate      = str(data['Receiver Governate'].iloc[id] or  "")  or "" ,
                    receiver_address_regionCity     = str(data['Receiver Region City'].iloc[id] or  "")  or "" ,
                    receiver_address_street         = str(data['Receiver Street'].iloc[id] or  "")  or "" ,
                    receiver_address_buildingNumber = str(data['Receiver Building Number'].iloc[id] or  "")  or "" ,
                )
                reciver.save() 
            except Exception as E :
                erros.append( str(E)  + " Erro Accourd in Adding Receiver" + str(data['Receiver Name'].iloc[id] or  "") )
        for i in erros :
                e = ErrorLog(
                    message = i ,
                    refrence = "Receiver"
                )
                e.save()
        if len(erros) > 1 :
            return ({"error" : "error"})
        return {"messgae" : "success"}
    except Exception as E :
        e = ErrorLog(
                message = E ,
                refrence = "Receiver"
            )
        e.save()
        return ({"error" : E})
@login_required(login_url='login')
def import_reciever(request) :
    page=  "import_reciever.html"
    content = {

    }
    if request.method== 'POST' :
        a =ReceiverFile(
            sheet =request.FILES['myfile'] )
        a.save()
        success = create_import_reciever(a.id , a.sheet.path)
        if success.get('error') :
            return redirect("errolog_list")
            # return render (request , "error.html" , {'message': success.get('error') })
        
        return redirect("reciever_list")    
    return render(request ,page , content  )
    

@login_required(login_url='login')
def reciever_list(request):
    page = 'receiver_list.html'
    recievers = Receiver.objects.all()
    if request.GET.get("search"):
        recievers = Receiver.objects.filter(Q(receiver_id__icontains=request.GET.get("search")  ) | Q(receiver_name__icontains=request.GET.get("search")))
    paginator = Paginator(recievers , 20)
    page_number = request.GET.get('page')
    invocies = paginator.get_page(page_number)
    content={
        'recievers' :invocies ,
        'search' : request.GET.get("search")
    }
    return render(request , page , content)


def creat_receiver(request):
    page = 'receiver.html'
    types = [{'v' :i[0] , 'n' :i[1] }
                for i in AccountType ]
    content ={
        'types' :types
    }

    if request.method=='POST':
        receiver = Receiver(
            name = request.POST.get('receiver_name') ,
            receiver_type = request.POST.get('receiver_type'),
            receiver_name = request.POST.get('receiver_name'),
            receiver_id = str(request.POST.get('receiver_id') or ''),
            receiver_address_branchId = str(request.POST.get('receiver_address_branchId') or '') , 
            receiver_address_country=request.POST.get('receiver_address_country'),
            receiver_address_governate =request.POST.get('receiver_address_governate'),
            receiver_address_regionCity =request.POST.get('receiver_address_regionCity'),
            receiver_address_street= request.POST.get('receiver_address_street'),
            receiver_address_buildingNumber = request.POST.get('receiver_address_buildingNumber')
        )
        receiver.save()
        return redirect('reciever_list')


    return render(request , page ,content)

def delete_receiver(request ,id):
    Receiver.objects.get(id =id).delete()
    return redirect('reciever_list')


def edit_receiver(request,id):
    recever = Receiver.objects.get(id = id)
    page = 'receiver.html'
    types = [{'v' :i[0] , 'n' :i[1] }
                for i in AccountType ]

    content  = {
        "receiver" : recever ,
        'types' : types
    }

    if request.method== "POST" :
            recever.name = request.POST.get('receiver_name') 
            recever.receiver_type = request.POST.get('receiver_type')
            recever.receiver_name = request.POST.get('receiver_name')
            recever.receiver_id = str(request.POST.get('receiver_id') or '')
            recever.receiver_address_branchId = str(request.POST.get('receiver_address_branchId') or '') 
            recever.receiver_address_country=request.POST.get('receiver_address_country')
            recever.receiver_address_governate =request.POST.get('receiver_address_governate')
            recever.receiver_address_regionCity =request.POST.get('receiver_address_regionCity')
            recever.receiver_address_street= request.POST.get('receiver_address_street')
            recever.receiver_address_buildingNumber = request.POST.get('receiver_address_buildingNumber')
            recever.save()
            return redirect('reciever_list')

    return render(request , page , content)


@login_required(login_url='login')
def errolog_list(request):
    page = 'error_list.html'
    errors = ErrorLog.objects.all().order_by('date')

    content = {
        "errors" :errors[0:100] if len(errors) > 100 else errors
    }
    return render(request , page , content )