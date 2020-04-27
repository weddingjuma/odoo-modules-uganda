# -*- coding: utf-8 -*-
{
    'name': "Cure Uganda",

    'summary': """
        Custom Odoo modules (addons) for CURE Children's Hospital of Uganda""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Cure International Inc.",
    'website': "https://www.cure.org",

    'category': 'Uncategorized',
    'version': '10.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','purchase','stock_no_negative','purchase_open_qty','purchase_order_approved','purchase_request','purchase_request_department','purchase_request_to_rfq','purchase_request_to_rfq_order_approved'],

    # always loaded
    'data': [
        'security/purchase_groups.xml',
        'security/ir.model.access.csv',
        'views/division_view.xml',
        'views/stock_dispense_view.xml',
        'views/util_views.xml'
    ],
}
