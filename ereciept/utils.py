
from collections import OrderedDict
import json
from hashlib import sha256
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


def round_decimal(x):
    return x


def serialize(key='', data={}):
    result = ""
    origin_key = key
    key = f'''"{(key or '').upper()}"''' if str(
        key or '').strip() != '' else ''
    # print("type(result)  =========> ", type(data))
    if type(data) in [list, ReturnList]:
        result += key
        for row in data:
            result += serialize(origin_key, row)

    elif type(data) in [dict, ReturnDict,OrderedDict]:
        result += key
        for k, v in data.items():
            result += serialize(k, v)
    else:
        if type(data) in [float]:
            data = round_decimal(data)
        
        # print("result  =========> "f'''{key}"{data}"''')
        result = f'''{key}"{data}"'''

    return result


def get_invoice_uuid(data):
    serialized_invoice = serialize(data=data)
    # print("serialized_invoice  ====> ", serialized_invoice)
    uuid = sha256(serialized_invoice.encode('utf-8')).hexdigest()
    return uuid
