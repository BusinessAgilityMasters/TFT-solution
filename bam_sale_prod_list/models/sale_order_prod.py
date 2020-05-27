# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
	bom_line_id = fields.Many2one('mrp.bom.line', string="BOM", store=True)

	def update_sol_qty(self):
		for prod in self:
			bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', prod.product_id.product_tmpl_id.id)],
												order="sequence desc", limit=1)
			ids = prod.sale_order_line_id.x_sale_order_line_ids.ids
			qty = prod.qty
			prod_ids = self.env['bam_sale_order_prod_list'].search([
				('parent_product_id', '=', prod.product_id.id),
				('id', 'in', ids)])
			for pi in prod_ids:
				bom_line_id = self.env['mrp.bom.line'].search([('bom_id', '=', bom_id.id),
															   ('product_id', '=', pi.product_id.id)],
															  limit=1)
				pi.qty = bom_line_id.product_qty * qty
				sub_bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', pi.product_id.product_tmpl_id.id)],
														order="sequence desc", limit=1)
				if sub_bom_id:
					product_id = pi.product_id
					self.update_sub_bom_products(product_id, sub_bom_id, ids)
				# pi.write({'qty': bom_line_id.product_qty * qty})

	def update_sub_bom_products(self, product_id, bom_id, ids):
		prod_ids = self.env['bam_sale_order_prod_list'].search([
			('parent_product_id', '=', product_id.id),
			('id', 'in', ids)])
		for pi in prod_ids:
			bom_line_id = self.env['mrp.bom.line'].search([('bom_id', '=', bom_id.id),
														   ('product_id', '=', pi.product_id.id)],
														  limit=1)
			# pi.write({'qty': bom_line_id.product_qty * self.qty})
			pi.qty = bom_line_id.product_qty * self.qty
			sub_bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', pi.product_id.product_tmpl_id.id)],
													order="sequence desc", limit=1)
			if sub_bom_id:
				product_id = pi.product_id
				self.update_sub_bom_products(product_id, sub_bom_id, ids)

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
