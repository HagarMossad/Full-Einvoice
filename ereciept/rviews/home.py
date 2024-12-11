from django.shortcuts import render ,redirect
from ereciept import models as tables
from django.core.paginator import Page, Paginator

Receiept = tables.ereciept.Receiept


def home(request) :
    receiepts = Receiept.objects.all().exclude(docstatus=-1).order_by("-id")
    active_receiept = Receiept.objects.filter(docstatus=-1)
    if request.GET.get("search_fdate"):
        receiepts =receiepts.filter(created_at__gte=request.GET.get("search_fdate")).order_by("-id")
    if request.GET.get("search_tdate"):
       receiepts=receiepts.filter(created_at__lte=request.GET.get("search_tdate")).order_by("-id")
    if request.GET.get("search_tdate"):
       receiepts=receiepts.filter(created_at__lte=request.GET.get("search_tdate")).order_by("-id")
    if request.GET.get("search_subid"):
       receiepts=receiepts.filter(submitionid=request.GET.get("search_subid")).order_by("-id")
    if request.GET.get("search_uuid"):
       receiepts=receiepts.filter(t_uid = request.GET.get("search_uuid")).order_by("-id")
    paginator = Paginator(receiepts  ,10)
    page_number = request.GET.get('page')
    receiepts_list = paginator.get_page(page_number)
    htmlpage = "pages/reciept_list.html"
    content = {
        "receiepts" : receiepts_list,
        "new_receiept" : active_receiept
    }
    return render(request ,htmlpage,content)


