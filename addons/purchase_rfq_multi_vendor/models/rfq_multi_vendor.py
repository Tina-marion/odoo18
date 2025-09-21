from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_ids = fields.Many2many('res.partner', string='Vendors', domain=[('supplier_rank', '>', 0)])
