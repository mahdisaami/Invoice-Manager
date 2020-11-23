from khayyam3 import JalaliDate
from rtl import rtl

from local_settings import DEFAULT_URL, DEFAULT_ADDRESS


def extract_data(invoice):
    data = {
        'base_url': DEFAULT_URL,
        'order_id': invoice.number,
        'address': DEFAULT_ADDRESS,
        'date': rtl(JalaliDate(invoice.date).strftime('%Y/%m/%d')),
        'pay_description': invoice.description,
        'customer': invoice.customer,
        'total_price': invoice.total_price,
        'items': len(invoice.entities),
        'details': invoice.entities,
        'discount': invoice.total_discount,
        'payable': invoice.payable_price

    }
    return data


factor_button = " <form method='POST'  action={action}  style='display: inline; padding;10px' target='_blank'> " \
                "<input type=hidden name='id' value={value}>" \
                "<button type=submit class='btn btn-{class_type}'> {text}</button>" \
                "</form>"
