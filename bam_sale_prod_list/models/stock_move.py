# -*- coding: utf-8 -*-

from odoo import models, fields


class StockMove(models.Model):
	_inherit = 'stock.move'

	x_sale_order_line_ids = fields.One2many(related="created_production_id.move_raw_ids", string="Components")
