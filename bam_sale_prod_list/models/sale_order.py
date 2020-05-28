from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError

import datetime
import pdb


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	x_mrp_production_qty  = fields.Integer(string="Qty of production", compute="_compute_qty_production")

	def _compute_qty_production(self):
		for so in self:
			MrpProduction_Obj = self.env['mrp.production']
			MrpProductions =  MrpProduction_Obj.search([('x_sale_order_id','=', so.id)])
			so.x_mrp_production_qty = len(MrpProductions)

	def _action_confirm(self):
		res = super(SaleOrder, self)._action_confirm()

		for so in self:
			for sol in so.order_line:
				if not sol.x_is_compose_sol:
					continue

			procurement_group_id = False
			Stock_Pickings = self.env['stock.picking'].search([('sale_id','=', so.id)])
			if len(Stock_Pickings) > 0:
				group_id = Stock_Pickings[0].group_id

			MrpBom = sol.x_mrp_bom_id
			if not MrpBom.id:
				MrpBom_Obj = self.env['mrp.bom']
				MrpBomLine_Obj = self.env['mrp.bom.line']
				GatherRouting = self.env.ref('bam_sale_prod_list.mrp_routing')
				code = sol.order_id.name + " " + sol.product_id.product_tmpl_id.name
				MrpBom = MrpBom_Obj.create({'x_sale_order_line_id' : sol.id,
										   'product_id'  : sol.product_id.id,
										   'product_tmpl_id' : sol.product_id.product_tmpl_id.id,
											'code' : code,
											'routing_id' : GatherRouting.id,
											})
				for sale_order_prod in sol.x_sale_order_line_ids:
					MrpBomLine_Obj.create({'bom_id' : MrpBom.id,
										   'product_id' : sale_order_prod.product_id.id,
										   'product_qty': sale_order_prod.qty,
										   'product_uom_id' : sale_order_prod.product_id.uom_id.id,
										   'sequence'  : sale_order_prod.sequence,
										   'x_name'  : sale_order_prod.name,
										   'x_level' : sale_order_prod.level,
										   'x_parent_product_id' : sale_order_prod.parent_product_id.id
					    					})
			Mrp_Production_Obj = self.env['mrp.production']
			Mrp_Production = False
			Mrp_Productions = Mrp_Production_Obj.search([('product_id','=', sol.product_id.id),
														 ('x_sale_order_line_id','=', sol.id),
														 ])
			if len(Mrp_Productions) > 0:
				Mrp_Production = Mrp_Productions[0]
			if not Mrp_Production:
				# name = so.name + " " + sol.product_id.name

				Mrp_Production  = Mrp_Production_Obj.create({'product_id' : sol.product_id.id,
														     'x_sale_order_line_id' : sol.id,
															 'product_uom_id' : sol.product_id.product_tmpl_id.uom_id.id,
															 'product_qty' : sol.product_uom_qty,
															 'bom_id'  : MrpBom.id,
															 'origin'  : so.name,
															 'procurement_group_id' : group_id.id,
														 })

			Stock_Move_Obj = self.env['stock.move']
			Stock_Moves =Stock_Move_Obj.search([('sale_line_id','=', sol.id)])
			print(Stock_Moves)
			for Stock_Move in Stock_Moves:
				Stock_Move.created_production_id = Mrp_Production
		return res

	@api.returns('self', lambda value: value.id)
	def copy(self, default=None):
		default = dict(default or {})
		res = super(SaleOrder, self).copy(default)
		for so in res:
			for orderline in so.order_line:
				if not orderline.x_is_compose_sol:
					continue
				else:
					orderline.set_default_parts()
		return res;

	def set_deliverydate_stock_picking(self):
		for so in self:
			for orderline in so.order_line:
				for prod in orderline.x_mrp_production_ids:
					if prod.state not in ('confirmed','planned'):
						continue
					prod.date_planned_start =  so.x_delivery_date
		return super(SaleOrder, self).set_deliverydate_stock_picking()



