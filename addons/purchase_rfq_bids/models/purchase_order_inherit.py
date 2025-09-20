from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    bid_ids = fields.One2many('purchase.bid', 'order_id', string='Vendor Bids')
    vendor_ids = fields.Many2many('res.partner', string='RFQ Vendors', domain=[('is_company', '=', True), ('supplier_rank', '>', 0)])
    is_rfq_multi_vendor = fields.Boolean(string='Multi-Vendor RFQ', default=False)
    winning_bid_id = fields.Many2one('purchase.bid', string='Winning Bid')
    
    def action_send_rfq_to_vendors(self):
        for order in self:
            if not order.vendor_ids:
                raise UserError(_("No vendors selected for this RFQ."))
            
            # Create bid records for each vendor
            for vendor in order.vendor_ids:
                existing_bid = self.env['purchase.bid'].search([
                    ('order_id', '=', order.id),
                    ('vendor_id', '=', vendor.id)
                ])
                if not existing_bid:
                    self.env['purchase.bid'].create({
                        'order_id': order.id,
                        'vendor_id': vendor.id,
                        'name': f"Bid-{order.name}-{vendor.name}",
                        'state': 'sent'
                    })
            
            logger.info(f"Created bid records for RFQ {order.name} - Vendors: {order.vendor_ids.mapped('name')}")
        return True
    
    def action_compare_bids(self):
        """Open bid comparison view"""
        return {
            'name': 'Compare Bids',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.bid',
            'view_mode': 'list',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id}
        }
