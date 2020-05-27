# -*- coding: utf-8 -*-

from odoo import models, fields


class Mrp_Production(models.Model):
	_inherit = 'mrp.production'

	x_sale_order_line_id = fields.Many2one('sale.order.line', "Sale order line")
	x_sale_order_id = fields.Many2one('sale.order', related="x_sale_order_line_id.order_id")

	def get_consumed_products(self):
		if self.bom_id and self.product_qty > 0:
			list_move_raw = [(4, move.id) for move in self.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
			moves_raw_values = self._get_moves_raw_values()
			move_raw_dict = {move.bom_line_id.id: move for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)}
			for move_raw_values in moves_raw_values:
				if move_raw_values['bom_line_id'] in move_raw_dict:
					list_move_raw += [(1, move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
				else:
					list_move_raw += [(0, 0, move_raw_values)]
			self.move_raw_ids = list_move_raw
		else:
			self.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]
