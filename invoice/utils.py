import datetime

import xlwt
import pandas as pd

from django.conf import settings

HEADER_SYTLE = xlwt.easyxf('font:bold on')
DEFAULT_STYLE = xlwt.easyxf()
CELL_STYLE_MAP = (
    (datetime.datetime, xlwt.easyxf(num_format_str="YYYY/MM/DD HH:MM")),
    (datetime.date, xlwt.easyxf(num_format_str='DD/MM/YYYY')),
    (datetime.time, xlwt.easyxf(num_format_str="HH:MM")),
    (bool, xlwt.easyxf(num_format_str="BOOLEAN")),
)




def queryset_to_workbook(queryset,
                         columns,
                         header_style=HEADER_SYTLE,
                         default_style=DEFAULT_STYLE,
                         cell_style_map=CELL_STYLE_MAP):
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    filepath = BASE_DIR / 'media/order.xlsx'

    data = []
    for i in queryset:
        val = [
            i.internalId,
            i.documentType,
            i.documentTypeVersion,
            str(i.dateTimeIssued),
            i.receiver_type,
            i.receiver_id,
            i.receiver_name,
            i.receiver_address_branchId,
            i.receiver_address_country,
            i.receiver_address_governate,
            i.receiver_address_regionCity,
            i.receiver_address_street,
            i.receiver_address_buildingNumber,
            i.netAmount,
            i.taxTotals,
            i.extraDiscountAmount,
            i.totalItemsDiscountAmount,
            i.totalAmount,
            i.totalSalesAmount,
            str(i.created_date),
            i.submissionId
        ]
        data.append(val)

    df = pd.DataFrame(data, columns=columns)
    for index, row in df.iterrows():
        if not row.submissionId:
            row.submissionId="Not Send"
        print(row['totalAmount'], row['submissionId'])
    with pd.ExcelWriter(filepath) as writer:
        df.to_excel(writer)

    path_url = settings.MEDIA_URL + 'order.xlsx'
    return path_url