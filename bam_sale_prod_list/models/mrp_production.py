from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError

import datetime
import pdb


class Mrp_Production(models.Model):
	_inherit = 'mrp.production'

	x_sale_order_line_id = fields.Many2one('sale.order.line', "Sale order line")
	x_sale_order_id = fields.Many2one('sale.order', related="x_sale_order_line_id.order_id")





