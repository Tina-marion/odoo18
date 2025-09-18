from odoo import models, fields

class PurchaseRequestBridge(models.Model):
    _inherit = "purchase.request"

    rfq_id = fields.Many2one(
        "purchase.order", string="Generated RFQ"
    )
