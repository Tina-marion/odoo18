from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # One-to-many relationship: One RFQ can have multiple bids
    bid_ids = fields.One2many(
        'purchase.bid',   # matches _name in purchase_bid.py
        'order_id',       # matches Many2one field in purchase_bid.py
        string='Vendor Bids'
    )
    
    # Many2many relationship: One RFQ can be sent to multiple vendors
    vendor_ids = fields.Many2many(
        'res.partner',
        string='RFQ Vendors',
        domain=[('is_company', '=', True), ('supplier_rank', '>', 0)]
    )
    
    # Track if this is an RFQ that needs vendor selection
    is_rfq_multi_vendor = fields.Boolean(
        string='Multi-Vendor RFQ',
        default=False
    )

    def action_send_rfq_to_vendors(self):
        """Send RFQ to selected vendors"""
        for order in self:
            if not order.vendor_ids:
                raise UserError(_("No vendors selected for this RFQ."))
            # Placeholder: replace with actual email logic later
            _logger.info(f"Sending RFQ {order.name} to vendors: {order.vendor_ids.mapped('name')}")
        return True

