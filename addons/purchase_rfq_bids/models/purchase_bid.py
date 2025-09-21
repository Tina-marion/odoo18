from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseBid(models.Model):
    _name = "purchase.bid"
    _description = "Purchase Bid"
    
    name = fields.Char(string="Bid Reference", required=True)
    order_id = fields.Many2one('purchase.order', string="RFQ", required=True)
    vendor_id = fields.Many2one('res.partner', string="Vendor", required=True)
    amount = fields.Float(string="Bid Amount")
    delivery_date = fields.Date(string="Promised Delivery Date")
    terms_conditions = fields.Text(string="Terms & Conditions")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent to Vendor'),
        ('received', 'Bid Received'),
        ('won', 'Won'),
        ('lost', 'Lost')
    ], string="Status", default='draft')
    is_winner = fields.Boolean(string="Winning Bid", default=False)
    
    def action_submit_bid(self):
        """Submit bid - Available for vendors"""
        for bid in self:
            if bid.state == 'draft':
                bid.state = 'received'
        return True
    
    def action_select_as_winner(self):
        """Select this bid as winner and create PO - Only for Procurement Users"""
        # Check if user has procurement rights
        if not self.env.user.has_group('purchase.group_purchase_user'):
            raise UserError(_('Only procurement users can select winning bids.'))
            
        for bid in self:
            # Mark this bid as winner
            bid.write({'state': 'won', 'is_winner': True})
            
            # Mark other bids for same RFQ as lost
            other_bids = self.env['purchase.bid'].search([
                ('order_id', '=', bid.order_id.id),
                ('id', '!=', bid.id)
            ])
            other_bids.write({'state': 'lost', 'is_winner': False})
            
            # Update the RFQ with winning vendor and amount
            bid.order_id.write({
                'partner_id': bid.vendor_id.id,
                'winning_bid_id': bid.id
            })
            
            # Update order lines with winning bid amount
            if bid.amount and bid.order_id.order_line:
                total_lines = len(bid.order_id.order_line)
                price_per_line = bid.amount / total_lines
                for line in bid.order_id.order_line:
                    line.price_unit = price_per_line
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Created Purchase Order',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'target': 'current',
        }
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': f'Bid from {bid.vendor_id.name} selected as winner!',
                'type': 'success'
            }
        }
    
    def action_submit_bid(self):
        """Mark bid as received from vendor"""
        self.write({'state': 'received'})
