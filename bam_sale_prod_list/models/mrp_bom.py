# -*- coding: utf-8 -*-

from odoo import models, fields


class Mrp_Production(models.Model):
	_inherit = 'mrp.bom'

	x_sale_order_line_id = fields.Many2one('sale.order.line', "Sale order line")
