# -*- coding: utf-8 -*-
{
    'name': "bam_sale_deliverydate",

    'summary': """
        This module will add a delivery date to the salesorder 
        """,

    'description': """
       
    """,

    'author': "Business Agility Masters",
    'website': "http://www.businessagilitymasters.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Base',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates/templates.xml',       
        'views/SaleOrder.xml'
      
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
