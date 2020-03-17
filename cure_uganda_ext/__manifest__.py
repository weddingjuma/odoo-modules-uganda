# -*- coding: utf-8 -*-
{
    'name': "Cure Uganda",

    'summary': """
        Custom Odoo modules (addons) for CURE Children's Hospital of Uganda""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Cure International Inc.",
    'website': "http://www.cure.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/util_views.xml'
    ],
}