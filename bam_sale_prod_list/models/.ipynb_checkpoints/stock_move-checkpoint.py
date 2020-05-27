from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError

import datetime
import pdb


class StockMove(models.Model):
	_inherit = 'stock.move'

	x_sale_order_line_ids = fields.One2many(related="created_production_id.move_raw_ids", string="Components")

