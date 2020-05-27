# -*- coding: utf-8 -*-
{
    'name': "bam_report_changes",

    'summary': """
        Report changes for TFT-Solutions""",

    'description': """
        Changes to the request for quotation being printed as Purchase Order
    """,

    'author': "Business Agility Masters",
    'website': "http://www.businessagilitymasters.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.9',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'report/purchase_order_report.xml'
    ],
}
