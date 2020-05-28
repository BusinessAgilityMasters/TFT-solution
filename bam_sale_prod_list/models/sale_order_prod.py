from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError

import datetime
import pdb


class bam_sale_order_prod(models.Model):
	_name = "bam_sale_order_prod_list"
	_order = 'level,parent_product_id, sequence'

	sequence = fields.Integer(name="sequence")
	sale_order_line_id = fields.Many2one('sale.order.line', required=True, ondelete="cascade")
	product_id = fields.Many2one('product.product', required=True)
	name = fields.Char(string="Description")
	qty = fields.Float(string="Qty")
	unit_price = fields.Float(string="Unit price")
	line_price = fields.Float(string="Line_price", compute="cmp_line_price")
	level = fields.Integer(string="Level", default=1)
	parent_product_id = fields.Many2one("product.product", string="Parent Product")


	@api.depends('qty', 'unit_price')
	def cmp_line_price(self):
		for object in self:
			object.line_price = object.qty * object.unit_price

	@api.onchange('product_id')
	def set_product_defaults(self):
		for object in self:
			if object.product_id.id:
				object.name = object.product_id.name
				object.unit_price = object.product_id.standard_price
