# -*- coding: utf-8 -*-
{
    'name': "bam_partner_creditcheck",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        To adjust the credit check application to the needs of TFT-Solutions
    """,

    'author': "Business Agility Masters",
    'website': "http://www.businessagilitymasters.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'contacts',
    'version': '0.9',

    # any module necessary for this one to work correctly
    'depends': ['base', 'partner_identification', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'data/res_partner_id_category_data.xml'
    ],
}
