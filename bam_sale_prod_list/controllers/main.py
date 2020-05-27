# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.sale_product_configurator.controllers.main import ProductConfiguratorController

class ProductConfiguratorControllerInherit(ProductConfiguratorController):

    def generate_parts_list_main(self, mrpbom, levelparts, level, parent_product_id, main_qty):
        mrp_bom_obj = request.env['mrp.bom']
        objects = []
        parent_product = request.env['product.product'].browse(parent_product_id)
        for mrpline in mrpbom.bom_line_ids:
            qty = mrpline.product_qty * main_qty
            values = {"product_id": mrpline.product_id,
                      "qty": qty,
                      "name": mrpline.product_id.name,
                      "unit_price": mrpline.product_id.standard_price,
                      # "sale_order_line_id": sol.id,
                      "level": level,
                      "bom_line_id": mrpline.id,
                      "parent_product": parent_product,
                      "parent_product_id": parent_product_id}
            objects.append(values)
            sub_boms = mrp_bom_obj.search([('product_tmpl_id', '=', mrpline.product_id.product_tmpl_id.id)])
            if len(sub_boms) > 0:
                subvalues = {"product_tmpl_id": mrpline.product_id.product_tmpl_id.id,
                             "level": level + 1,
                             "product_id": mrpline.product_id.id,
                             "qty": qty}
                levelparts.append(subvalues)
        return {'levelparts': levelparts, 'objects': objects};

    def _show_optional_products(self, product_id, variant_values, pricelist, handle_stock, **kw):
        product = request.env['product.product'].browse(int(product_id))
        combination = request.env['product.template.attribute.value'].browse(variant_values)
        add_qty = int(kw.get('add_qty', 1))
        no_variant_attribute_values = combination.filtered(
            lambda product_template_attribute_value: product_template_attribute_value.attribute_id.create_variant == 'no_variant'
        )
        if no_variant_attribute_values:
            product = product.with_context(no_variant_attribute_values=no_variant_attribute_values)

        if kw.get('kwargs').get('context').get('default_sale_order_line_id'):
            sale_order_line = request.env['sale.order.line'].sudo().search([('id','=',int(kw.get('kwargs').get('context').get('default_sale_order_line_id')))])
            mrp_boms_obj = []
            for x_sale_order_line_id in sale_order_line.x_sale_order_line_ids:
                x_sale_order_line_id_dic = {}
                x_sale_order_line_id_dic['product_id'] = x_sale_order_line_id.product_id
                x_sale_order_line_id_dic['qty'] = x_sale_order_line_id.qty
                x_sale_order_line_id_dic['level'] = x_sale_order_line_id.level
                x_sale_order_line_id_dic['unit_price'] = x_sale_order_line_id.unit_price
                x_sale_order_line_id_dic['parent_product'] = x_sale_order_line_id.parent_product_id
                mrp_boms_obj.append(x_sale_order_line_id_dic)
        else:
        #get the bill of material for product
            mrp_bom_obj = request.env['mrp.bom']

            levelparts = []
            objects = []
            values = {'objects' : None}
            levelparts.append({"product_tmpl_id": product.product_tmpl_id.id,
                               "level": 1, "product_id": product.id, "qty": 1})
            while len(levelparts) > 0:
                levelpart = levelparts[0]
                del levelparts[0]
                product_tmpl_id = levelpart['product_tmpl_id']
                mrp_boms = mrp_bom_obj.search([('product_tmpl_id', '=', product_tmpl_id)], order="sequence")
                if len(mrp_boms) == 0:
                    continue
                mrpbom = mrp_boms[0]
                level = levelpart["level"]
                parent_product_id = levelpart["product_id"]
                qty = levelpart["qty"]
                values = self.generate_parts_list_main(mrpbom, levelparts, level, parent_product_id, qty)
                levelparts = values['levelparts']
                objects.extend(values['objects'])

            mrp_boms_obj = None
            if values['objects']:
                mrp_boms_obj = objects
        return request.env['ir.ui.view'].render_template("sale_product_configurator.optional_products_modal", {
            'product': product,
            'combination': combination,
            'add_qty': add_qty,
            'parent_name': product.name,
            'pricelist': pricelist,
            'handle_stock': handle_stock,
            'mrp_boms_main' : mrp_boms_obj
        })
