from odoo import models, fields, api

class PurchaseBid(models.Model):
    _name = "purchase.rfq.bid"
    _description = "Supplier Bid for RFQ"

    rfq_id = fields.Many2one(
        "purchase.order", string="Related RFQ", required=True, ondelete="cascade"
    )
    vendor_id = fields.Many2one(
        "res.partner", string="Vendor", required=True, domain=[("supplier_rank", ">", 0)]
    )
    product_id = fields.Many2one(
        "product.product", string="Product", required=True
    )
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    price_unit = fields.Float(string="Unit Price", required=True)
    total = fields.Monetary(
        string="Total", compute="_compute_total", store=True, currency_field="currency_id"
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", required=True,
        default=lambda self: self.env.company.currency_id
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        string="Status", default="draft"
    )

    @api.depends("quantity", "price_unit")
    def _compute_total(self):
        for bid in self:
            bid.total = bid.quantity * bid.price_unit
