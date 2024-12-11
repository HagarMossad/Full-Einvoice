from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from invoice.column import create_e_invoice
# Create your views here.

@csrf_exempt
def recive_invoice_data(request):
    data = json.loads(request.body)
    r=create_e_invoice(data[0])
    if r.get("creates") == "created":
        return HttpResponse(status=200)

