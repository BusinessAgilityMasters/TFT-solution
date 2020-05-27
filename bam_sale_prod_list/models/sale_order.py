# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, ValidationError, Warning


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
		for order in self:
			for line in order.order_line:
				if not line.x_is_compose_sol:
					continue

				procurement_group_id = False
				Stock_Pickings = self.env['stock.picking'].search([('sale_id','=', order.id)])
				if len(Stock_Pickings) > 0:
					group_id = Stock_Pickings[0].group_id

				MrpBom = line.x_mrp_bom_id
				if not MrpBom.id:
					MrpBom_Obj = self.env['mrp.bom']
					MrpBomLine_Obj = self.env['mrp.bom.line']
					GatherRouting = self.env.ref('bam_sale_prod_list.mrp_routing')
					code = line.order_id.name + " " + line.product_id.product_tmpl_id.name
					MrpBom = MrpBom_Obj.create({'x_sale_order_line_id' : line.id,
											   'product_id'  : line.product_id.id,
											   'product_tmpl_id' : line.product_id.product_tmpl_id.id,
												'code' : code,
												'routing_id' : GatherRouting.id})
					for sale_order_prod in line.x_sale_order_line_ids:
						MrpBomLine_Obj= MrpBomLine_Obj.create({'bom_id' : MrpBom.id,
											   'product_id' : sale_order_prod.product_id.id,
											   'product_qty': sale_order_prod.qty,
											   'product_uom_id' : sale_order_prod.product_id.uom_id.id,
											   'sequence'  : sale_order_prod.sequence,
											   'x_name'  : sale_order_prod.name,
											   'x_level' : sale_order_prod.level,
											   'x_parent_product_id' : sale_order_prod.parent_product_id.id,
											   'bam_so_prod_list_id': sale_order_prod.id or False})
				Mrp_Production_Obj = self.env['mrp.production']
				Mrp_Production = False
				Mrp_Productions = Mrp_Production_Obj.search([('product_id','=', line.product_id.id),
															 ('x_sale_order_line_id','=', line.id)])
				if len(Mrp_Productions) > 0:
					Mrp_Production = Mrp_Productions[0]
				if not Mrp_Production:
					# name = order.name + " " + line.product_id.name
					Mrp_Production  = Mrp_Production_Obj.create({'product_id' : line.product_id.id,
																 'x_sale_order_line_id' : line.id,
																 'product_uom_id' : line.product_id.product_tmpl_id.uom_id.id,
																 'product_qty' : line.product_uom_qty,
																 'bom_id'  : MrpBom.id or False,
																 'origin'  : order.name,
																 'procurement_group_id' : group_id.id})
				Mrp_Production.get_consumed_products()
				line.write({'production_id': Mrp_Production.id or False})

				Stock_Move_Obj = self.env['stock.move']
				Stock_Moves =Stock_Move_Obj.search([('sale_line_id','=', line.id)])
				for Stock_Move in Stock_Moves:
					Stock_Move.created_production_id = Mrp_Production
		return res

	def update_production_order(self):
		for order in self:
			# mrp_id = self.env['mrp.production'].search([('x_sale_order_id', '=', order.id)])
			# if mrp_id.state != 'draft':
			# 	raise Warning(_("You can not update Production which is already in %s state.") % (mrp_id.state))
			for line in order.order_line:
				if line.production_id.state != 'draft':
					raise Warning(_("You can not update Production which is already in %s state.") % (line.production_id.state))
				bom_id = line.x_mrp_bom_id or False
				for prod_line in line.x_sale_order_line_ids:
					if prod_line.id not in bom_id.bom_line_ids.mapped('bam_so_prod_list_id').ids:
						self.env['mrp.bom.line'].create(
							{'bom_id': bom_id.id,
							 'product_id': prod_line.product_id.id,
							 'product_qty': prod_line.qty,
							 'product_uom_id': prod_line.product_id.uom_id.id,
							 'sequence': prod_line.sequence,
							 'x_name': prod_line.name,
							 'x_level': prod_line.level,
							 'x_parent_product_id': prod_line.parent_product_id.id,
							 'bam_so_prod_list_id': prod_line.id or False})
					else:
						bom_line_id = self.env['mrp.bom.line'].search([
							('bom_id', '=', bom_id.id),
							('bam_so_prod_list_id', '=', prod_line.id)],
							limit=1)
						bom_line_id.write({"product_qty": prod_line.qty})
				bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', bom_id.id),
												 ('bam_so_prod_list_id', 'not in', line.x_sale_order_line_ids.ids)])
				bom_line_ids.unlink()
				if line.production_id.state == 'draft':
					line.production_id.write({'product_qty': line.product_uom_qty or 1.0})
					line.production_id.get_consumed_products()

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



