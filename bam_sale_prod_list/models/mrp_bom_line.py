# -*- coding: utf-8 -*-

from odoo import models, fields


class Mrp_Production(models.Model):
	_inherit = 'mrp.bom.line'

	x_name = fields.Char(string="Description")
	x_level = fields.Integer(string="Level", default=1)
	x_parent_product_id = fields.Many2one("product.product", string="Parent Product")
	bam_so_prod_list_id = fields.Many2one('bam_sale_order_prod_list')