from odoo import models, fields, api
from odoo.exceptions import except_orm, ValidationError


class bam_salesorder(models.Model):
       
    _inherit = 'sale.order'
    x_delivery_date = fields.Datetime(string="Planned Delivery date", default=fields.Datetime.now())
    x_calendar_date = fields.Datetime(compute="_compute_calendar_date");
    
    @api.depends('x_delivery_date')
    def _compute_calendar_date(self):
        state = self.state;
        if (state):
            if (state == 'done' or state == 'sale'):  
                self.x_calendar_date = self.x_delivery_date;
                return;
        self.x_calendar_date = self.validity_date;
    
    def action_confirm(self):
        res = super(bam_salesorder, self).action_confirm()
        for so in self:
            so.set_deliverydate_stock_picking();
        return res    
    
    def write(self, values):
        res = super(bam_salesorder, self).write(values);
        if (res):
             if 'x_delivery_date' in values:
                 for so in self:
                     so.set_deliverydate_stock_picking();
        return res;

    def set_deliverydate_stock_picking(self):
        for so in self:
            for picking_id in so.picking_ids:
                for stock_picking in picking_id:
                    if stock_picking.state not in ['done','cancel']:
                        stock_picking.scheduled_date = so.x_delivery_date
                        stock_picking.min_date = so.x_delivery_date;
           
    
    
               
    
