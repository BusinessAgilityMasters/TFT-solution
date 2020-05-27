from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError

import datetime
import pdb


class Mrp_Production(models.Model):
	_inherit = 'mrp.bom.line'

	x_name = fields.Char(string="Description")
	x_level = fields.Integer(string="Level", default=1)
	x_parent_product_id = fields.Many2one("product.product", string="Parent Product")