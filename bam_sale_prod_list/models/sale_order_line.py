# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError
from . import sale_order_prod

import datetime


class sale_order_line(models.Model):
	_inherit = "sale.order.line"

	x_sale_order_line_ids 	= fields.One2many('bam_sale_order_prod_list', 'sale_order_line_id', copy=False)
	x_mrp_bom_ids			= fields.One2many('mrp.bom','x_sale_order_line_id', string="Mrp bom")
	x_calc_total 			= fields.Float(string="Calculation total", compute="cmp_calc_total")
	x_is_compose_sol 		= fields.Boolean(string="Is compose sol",compute="_compute_compose_sol")
	x_mrp_production_ids  	= fields.One2many('mrp.production','x_sale_order_line_id', string="Production")
	x_mrp_bom_id			= fields.Many2one('mrp.bom', compute="_compute_mrp_bom_id")
	production_id = fields.Many2one('mrp.production', "Production")



	def write(self, vals):
		if vals.get('x_sale_order_line_ids'):
			if self.x_sale_order_line_ids:
				for x_sale_order_line_id in self.x_sale_order_line_ids:
					x_sale_order_line_id.unlink()
		return super(sale_order_line,self).write(vals)



	def _compute_mrp_bom_id(self):
		for sol in self:
			x_mrp_bom_id = False
			for mrpbom in sol.x_mrp_bom_ids:
				if mrpbom.product_id.id == sol.product_id.id:
					x_mrp_bom_id = mrpbom
			sol.x_mrp_bom_id = x_mrp_bom_id

	@api.onchange('product_id')
	def _compute_compose_sol(self):
		for object in self:
			x_is_compose_sol = False
			if object.product_id.id:
			   route_eto = self.env.ref('bam_sale_prod_list.stock_location_route_eto')
			for route_id in object.product_id.product_tmpl_id.route_ids:
				if route_id.id == route_eto.id:
					x_is_compose_sol = True
			object.x_is_compose_sol = x_is_compose_sol

	def cmp_calc_total(self):
		for object in self:
			calc_total = 0
			for line in object.x_sale_order_line_ids:
				calc_total = calc_total + line.line_price
			object.x_calc_total = object.product_uom_qty * calc_total

	@api.onchange('product_id')
	def set_default_parts(self):
		print ("vcccccc===============", self._context)
		for sol in self:
			if not self._context.get('default_x_sale_order_line_ids'):
				print("sol=================================",sol)
				print("sol=================================",sol.product_id)
				print("sol=================================",sol.product_id.product_tmpl_id)
				if sol.product_id.id == False:
					continue
				has_route_eto = False
				route_eto = self.env.ref('bam_sale_prod_list.stock_location_route_eto')
				for route_id in sol.product_id.product_tmpl_id.route_ids:
					if route_id.id == route_eto.id:
						has_route_eto = True
				if not has_route_eto:
					continue
				for calcline in sol.x_sale_order_line_ids:
					calcline.unlink()
				mrp_bom_obj = self.env['mrp.bom']
				levelparts = []
				objects = []
				levelparts.append({"product_tmpl_id" : sol.product_id.product_tmpl_id.id, "level" : 1, "product_id" :sol.product_id.id, "qty": 1})
				while len(levelparts) > 0:
					levelpart = levelparts[0]
					del levelparts[0]
					product_tmpl_id = levelpart['product_tmpl_id']
					print("product_tmpl_id==================", product_tmpl_id)
					mrp_boms = mrp_bom_obj.search([('product_tmpl_id', '=', product_tmpl_id)],
												  order="sequence")
					print("mrp_boms==================", mrp_boms)
					if len(mrp_boms) == 0:
						continue
					mrpbom = mrp_boms[0]
					level = levelpart["level"]
					parent_product_id = levelpart["product_id"]
					qty = levelpart["qty"]
					values = self.generate_parts_list(mrpbom, levelparts, sol, level, parent_product_id, qty)
					levelparts = values['levelparts']
					objects.extend(values['objects'])
				print("objects>>>>>>", objects)
				sol.x_sale_order_line_ids = objects
#  				
# 			else:
# 				print("sol=================================",sol)
# 				print("sol=================================",sol.product_id)
# 				print("sol=================================",sol.product_id.product_tmpl_id)
# 				xsolids = self._context.get('default_x_sale_order_line_ids')
# 				print ("eval>>>>>>>>>", xsolids[2])
# # 				xsolids[]
#   
# 				vc = {} #{'sale_order_line_id':sol}
# 				for key, value in xsolids[2].items():
# 					vc.update({
# 						key: value
# 					})
# 				vc.update({
# 					'product_tmpl_id': sol.product_id.product_tmpl_id.id
# 				})
# 				mrp_bom_obj = self.env['mrp.bom']
# 				levelparts = []
# 				objects = []
# 				levelparts.append(vc)
# 				while len(levelparts) > 0:
# 					levelpart = levelparts[0]
# 					del levelparts[0]
# 					product_tmpl_id = levelpart['product_tmpl_id']
# 					print("product_tmpl_id==================", product_tmpl_id)
# 					mrp_boms = mrp_bom_obj.search([('product_tmpl_id', '=', product_tmpl_id)],
# 												  order="sequence")
# 					print("mrp_boms==================", mrp_boms)
# 					if len(mrp_boms) == 0:
# 						continue
# 					mrpbom = mrp_boms[0]
# 					level = levelpart["level"]
# 					parent_product_id = levelpart["parent_product_id"]
# 					qty = levelpart["qty"]
# 					values = self.generate_parts_list(mrpbom, levelparts, sol, level, parent_product_id, qty)
# 					levelparts = values['levelparts']
# 					objects.extend(values['objects'])
# 				print("objects>>>>>>", objects)
# 				sol.x_sale_order_line_ids = objects

# 
# 			elif self._context.get('bam_configurator'):
# 				mainProduct = self._context.get('configurator_main')[0]
# 				if sol.product_id.id == False:
# # 					sol.product_id = self.env['product.product'].search([('id', '=', mainProduct.get('product_id'))])
# 					if mainProduct.get('quantity'):
# 						mainProduct['product_uom_qty'] = mainProduct['quantity']
# 						mainProduct.pop('quantity')
# 					sol.write(mainProduct)
					
# 				print("sol=================================",sol)
# 				print("sol=================================",sol.product_id)
# 				print("sol=================================",sol.product_id.product_tmpl_id)
# 					
# 					
# 				has_route_eto = False
# 				route_eto = self.env.ref('bam_sale_prod_list.stock_location_route_eto')
# 				for route_id in sol.product_id.product_tmpl_id.route_ids:
# 					if route_id.id == route_eto.id:
# 						has_route_eto = True
# 					if not has_route_eto:
# 						continue
# 				for calcline in sol.x_sale_order_line_ids:
# 					calcline.unlink()
# 				mrp_bom_obj = self.env['mrp.bom']
# 				levelparts = []
# 				objects = []
# 				levelparts.append({"product_tmpl_id" : sol.product_id.product_tmpl_id.id, "level" : 1, "product_id" :sol.product_id.id, "qty": 1})
# 				while len(levelparts) > 0:
# 					levelpart = levelparts[0]
# 					del levelparts[0]
# 					product_tmpl_id = levelpart['product_tmpl_id']
# 					print("product_tmpl_id==================", product_tmpl_id)
# 					mrp_boms = mrp_bom_obj.search([('product_tmpl_id', '=', product_tmpl_id)],
# 												  order="sequence")
# 					print("mrp_boms==================", mrp_boms)
# 					if len(mrp_boms) == 0:
# 						continue
# 					mrpbom = mrp_boms[0]
# 					level = levelpart["level"]
# 					parent_product_id = levelpart["product_id"]
# 					qty = levelpart["qty"]
# 					values = self.generate_parts_list(mrpbom, levelparts, sol, level, parent_product_id, qty)
# 					levelparts = values['levelparts']
# 					objects.extend(values['objects'])
# 				print("objects>>>>>>", objects)
# 				sol.x_sale_order_line_ids = objects



	def generate_parts_list(self, mrpbom, levelparts, sol, level, parent_product_id, main_qty):
		mrp_bom_obj = self.env['mrp.bom']
		objects = []

		for mrpline in mrpbom.bom_line_ids:
			qty = mrpline.product_qty * main_qty
			values = {"product_id": mrpline.product_id.id,
					  "qty": qty,
					  "name": mrpline.product_id.name,
					  "unit_price": mrpline.product_id.standard_price,
					  "sale_order_line_id": sol.id,
					  "level": level,
					  "bom_line_id": mrpline.id,
					  "parent_product_id" : parent_product_id}
			objects.append((0, 0, values))
			sub_boms = mrp_bom_obj.search([('product_tmpl_id', '=', mrpline.product_id.product_tmpl_id.id)])
			if len(sub_boms) > 0:
				subvalues = {"product_tmpl_id": mrpline.product_id.product_tmpl_id.id,
							 "level": level + 1,
							 "product_id": mrpline.product_id.id,
							 "qty": qty}
				levelparts.append(subvalues)
		return {'levelparts' : levelparts, 'objects': objects};

	def _check_routing(self):
		route_eto = self.env.ref('bam_sale_prod_list.stock_location_route_eto')
		for route_id in self.product_id.product_tmpl_id.route_ids:
			if route_id.id == route_eto.id:
				return True
		return super(sale_order_line, self)._check_routing()
