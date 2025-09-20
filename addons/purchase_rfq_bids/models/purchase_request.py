from odoo import models, fields, api, _

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    
    name = fields.Char(string='Request Reference', required=True, default='New')
    employee_id = fields.Many2one('res.users', string='Requesting Employee', required=True, default=lambda self: self.env.user)
    request_date = fields.Date(string='Request Date', default=fields.Date.context_today)
    reason = fields.Text(string='Request Reason', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='draft', string='Status')
    
    def action_submit(self):
        self.write({'state': 'submitted'})
    
    def action_approve(self):
        self.write({'state': 'approved'})
    
    def action_reject(self):
        self.write({'state': 'rejected'})
