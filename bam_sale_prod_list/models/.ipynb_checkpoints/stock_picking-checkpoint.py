from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError

import datetime
import pdb


class StockPicking(models.Model):
	_inherit = 'stock.picking'

	x_mrp_production_qty = fields.Integer(string="Qty of production", compute="_compute_qty_production")

	def button_validate(self):
		self.process_mrp_production()
		return super(StockPicking, self).button_validate()

	def action_assign(self):
		return super(StockPicking, self).action_assign()

	def process_mrp_production(self):
		for sp in self:
			print(sp)
			for move in sp.move_ids_without_package:
				if len(move.x_sale_order_line_ids) == 0:
					continue
				move.created_production_id.action_assign()
				if move.created_production_id.state == 'confirmed':
				   move.created_production_id.button_plan()
				wos = self.env['mrp.workorder'].search([('production_id', '=', move.created_production_id.id)])
				for wo in wos:
					if wo.state in ('done'):
						continue
					wo.open_tablet_view()
					wo.do_finish()
				move.created_production_id.button_mark_done()




