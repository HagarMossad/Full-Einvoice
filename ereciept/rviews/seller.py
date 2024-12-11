from django.shortcuts import render ,redirect
from ereciept.models import Seller


def seller_list(request) :
    profile = None
    profile = Seller.objects.all().first()
    if request.method == "GET" :
       pass
    if request.method == "POST" :
        data = request.POST
        if not profile :
            profile = Seller()

        profile.rin =data.get("rin") 
        profile.companyTradeName = data.get("companyTradeName")
        profile.branchCode = data.get("branchCode")
        profile.country = data.get("country")
        profile.governate = data.get("governate")
        profile.regionCity = data.get("regionCity")
        profile.street = data.get("street")
        profile.buildingNumber = data.get("buildingNumber")
        profile.deviceSerialNumber  = data.get("deviceSerialNumber")
        profile.activityCode = data.get("activityCode")
        profile.save()
    page = "pages/seller.html"
    content = {
        "profile" : profile
    }
    return render(request , page ,content)




