# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class SaleProductConfiguratorInherit(models.TransientModel):
    _inherit = 'sale.product.configurator'
    sale_order_line_id = fields.Many2one('sale.order.line', string="Order Line")

# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#     website_form_enable_metadata = fields.Boolean(related="website_id.website_form_enable_metadata", readonly=False)
