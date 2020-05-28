from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError

import datetime
import pdb


class Mrp_Production(models.Model):
	_inherit = 'mrp.bom'

	x_sale_order_line_id = fields.Many2one('sale.order.line', "Sale order line")