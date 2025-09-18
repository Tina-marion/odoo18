from odoo import models, fields, api

class PurchaseBid(models.Model):
    _name = "purchase.bid"
    _description = "Purchase Bid"

    name = fields.Char(string="Bid Reference")
    amount = fields.Float(string="Amount")
    order_id = fields.Many2one('purchase.order', string="Purchase Order")  # fixed

    @api.model
    def create_bid(self, order_id, amount):
        """Example method to create a bid"""
        return self.create({
            'order_id': order_id,
            'amount': amount,
        })
