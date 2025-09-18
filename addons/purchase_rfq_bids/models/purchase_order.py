from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Link RFQ to multiple bids
    bid_ids = fields.One2many('purchase.bid', 'rfq_id', string='Bids')

    # Method called by your XML button
    def action_send_rfq_to_vendors(self):
        for order in self:
            # For now, just log for testing
            _logger = self.env['ir.logging']
            _logger.create({
                'name': 'Send RFQ',
                'type': 'server',
                'dbname': self.env.cr.dbname,
                'level': 'INFO',
                'message': f'Sending RFQ for order {order.name}',
                'path': 'purchase.order',
            })
        return True
