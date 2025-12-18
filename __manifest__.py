# -*- coding: utf-8 -*-
{
    'name': "Bramalea extras",
    'summary': """
        Bramalea extras""",
    'description': """
       Bramalea extra tools
    """,
    'author': "Jefferson Silva",
    'website': "",
    'category': 'Uncategorized',
    'version': '17.1.0',
    'license': 'LGPL-3',
    'depends': ['stock', 'product', 'sale'],
    'data': [
        'views/purchase_order_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'wizard/update_products_wizard.xml',
    ],
    'installable': True,
    'aplication' : False,
}
