import json 
f = open("/home/beshoy/taxauth/E-recirpt-app/receiptproject/ereciept/models/taxtypes.json")
json_data = json.load(f)
data = [(i.get("code"), i.get("Desc_en")) for i in json_data ]
print(data)