# -*- coding: utf-8 -*-
{
	'name': "bam_sale_prod_list",

	'summary': """
	Integrates the materials of the salesorder with the production order 
        """,

	'description': """
          
    """,

	'author': 'Business Agility Masterse',
	'website': "http://www.businessagilitymasters.com",

	# Categories can be used to filter modules in modules listing
	# Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
	# for the full list
	'category': 'Tools',
	'version': '0.1',

	# any module necessary for this one to work correctly
	'depends': ['sale_management','mrp','sale_stock','bam_sale_deliverydate','sale_product_configurator', 'account'],

	# always loaded
	'data': [
		'views/assets.xml',
		'wizard/sale_product_configurator_views.xml',
		'views/sale_order_prod.xml',
		'views/mrp_production.xml',
		'views/sale_order.xml',
		'views/stock_move.xml',
		'views/data.xml',
		'views/mrp_bom.xml',
		'views/templates.xml',
		'security/ir.model.access.csv',
		
	],
	# only loaded in demonstration mode
	'demo': [
		'demo/demo.xml',
	],
}