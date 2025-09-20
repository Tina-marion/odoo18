from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    
    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, default=lambda self: 'PR/')
    requester_id = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user)
    date_request = fields.Datetime(string='Request Date', default=fields.Datetime.now)
    line_ids = fields.One2many('purchase.request.line', 'request_id', string='Request Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('done', 'Done')
    ], string='Status', default='draft')

    def action_submit(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'

    @api.model
    def create(self, vals):
        if vals.get('name', 'PR/') == 'PR/':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'PR/'
        return super(PurchaseRequest, self).create(vals)
