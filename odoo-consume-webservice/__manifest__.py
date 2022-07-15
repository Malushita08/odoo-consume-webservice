# -*- coding: utf-8 -*-
{
    'name': "odoo-consume-webservice",

    'summary': """
        CONSUMIR UN WEB SERVICE""",

    'description': """
        CONSUMIR UN WEB SERVICEE
    """,

    'author': "MALUS",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/kds_web_service.xml',
    ],
}
